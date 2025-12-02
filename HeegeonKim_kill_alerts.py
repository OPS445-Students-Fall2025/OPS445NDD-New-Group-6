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
