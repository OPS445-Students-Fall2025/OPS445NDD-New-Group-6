#!/usr/bin/env python3
""" 

Process management system
Member: Heegeon Kim
Student ID: hkim352

# references: Lab 4 - strings, lists, tuples, OS module, lab 5 - file I/O, exception handling, lab 6 - classes and objects, lab 7 - functions, scope, time objects
"""
import os
import signal
import subprocess

print("Process Management System starting!")

def readmemoryinfo():
    """read memory information from /proc/meminfo, returns dictionary with memory values"""

    memorydata = {}

    #checking if the file exists first
    if os.path.exists('/proc/meminfo'):
        fileobject = open('/proc/meminfo', 'r')
        content = fileobject.read()
        fileobject.close()

        lines = content.split('\n')
        for line in lines:
            if ':' in line:
                parts = line.split(':')
                key = parts[0].strip()
                valuepart = parts[1].strip()

                #just getting the number value 
                numbers = []
                for word in valuepart.split():
                    if word.isdigit():
                        numbers.append(word)

                if numbers:
                    memorydata[key] = int(numbers[0])
    else:
        print("/proc/meminfo was not found")

    return memorydata

def getmemoryusage():
    """calculate memory usage percentage simple math operations"""
    
    memorydata = readmemoryinfo()

    total = memorydata.get('totalmemory', 0)
    available = memorydata.get('memoryavailable', 0)

    if total == 0:
        print("Could not get total memory")
        return 0.0

    used = total - available
    percent = (used / total) * 100

    # round to 2 decimal places

    return round(percent, 2)


def checkthreshold(limit):
    """ check if memory exceeds limit and then returns true or false"""

    current = getmemoryusage()

    if current > limit:
        
        print(f"memory at {current}% (limit: {limit}%)")
        return True, current
    
    else:
        
        print(f"memory at {current}% (limit: {limit}%)")
        return False, current


def getprocesslist():
    """get list of process using ps command"""

    processes = []

    # run ps command
    cmd = ['ps', 'aux']
    result = subprocess.run(cmd, captureoutput=True, text=True)

    if result.returncode == 0:
        lines = result.stdout.split('\n')

        #skip header
        for line in lines[1:]:
            if line.strip():
                parts = line.split(maxsplit=10)
                if len(parts) >= 11:
                    processinfo = {
                            'user': parts[0],
                            'pid': int(parts[1]),
                            'cpu': float(parts[2]),
                            'mem': float(parts[3]),
                            'cmd': parts[10]
                    }
                    processes.append(processinfo)

    else:
        print("error running ps command")

    return processes

def sortbymemory(processes, count=5):
    """ sort processes by memory usage"""

    if not processes:
        return []

    #create a copy to sort
    sortedlist = processes[:]

    #simple bubble sort 
    for i in range(len(sortedlist)):
        for j in range(len(sortedlist)-1):
            if sortedlist[j]['mem'] < sortedlist[j+1]['mem']:

                #swap
                temp = sortedlist[j]
                sortedlist[j] = sortedlist[j+1]
                sortedlist[j+1] = temp

    return sortedlist[:count]


def killpid(pid, forcekill=False):
    """ kill process by PID and simple error checking """

    #validation
    if not isinsistance(pid, int):
        return False, "PID must be an integer"

    if pid <= 0:
        return Flase, "PID must be positive"

    #check if process exists 
    if not os.path.exists(f'/proc/{pid}'):
        return False, f"Process {pid} does not exist"

    #making sure not to kill important processes
    if pid < 100:
        return False, f"PID {pid} is a system process"

    #don't kill this process itself
    if pid == os.getpid():
        return False, "Cannot kill this current process"

    #force kill
    if forcekill:
        os.kill(pid, signal.SIGKILL)
        return True, f"FOrce killed process {pid}"

    else:
        os.kill(pid, signal.SIGTERM)
        return True, f"Sent termination to process {pid}"


#global variables for alerts
alertcount = 0
lastalerttime = None

def showalert(message, alerttype="INFO"):
    """ simple alert function"""

    global alertcount, lastalerttime

    #timestamp
    import time
    timestamp = time.strftime("%H:%M:%S")

    #format message
    formatted = f"[{timestamp}] [{alerttype}] {message}"
    print(formatted)

    #log to file
    logfile = open("memoryalerts.txt", "a")
    logfile.write(formatted + "\n")
    logfile.close()

    #update counters
    alertcount += 1
    lastalerttime = timestamp

    return True

def checkandalert(limit=80.0):
    """check memory and show alert if needed"""

    current = getmemoryusage()

    if current > limit:
        showalert(f"Memory at {current}% exceeds {limit}%", "warning")
        return True, current
    else:
        showalert(f"Memory at {current}% is OK", "info")
        return False, current



