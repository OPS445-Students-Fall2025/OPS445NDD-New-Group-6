#!/usr/bin/env python3
""" 

Output Formatting and Reports
Author ID:ssharma608

# references: Lab 5-exceptions and errors, Lab 4-strings and substrings, Assignment 2-version B    """


def show_memory(percent, limit):
    """Show memory info"""
    print("System Health Report")
    print("====================")
    print()
    print("Memory Information:")
    print("-------------------")
    print("Used: " + str(percent) + "%")
    
    if percent >= limit:
        print("Status: BAD")
    elif percent >= limit - 10:
        print("Status: WARNING")
    else:
        print("Status: OK")
    
    print()

def show_processes(processes, count):
    """Show process list"""
    print("Top " + str(count) + " Processes:")
    print("----------------------")
    
    if len(processes) == 0:
        print("No processes")
        print()
        return
    
    # Show only first 'count' processes
    show_this_many = count
    if count > len(processes):
        show_this_many = len(processes)
    
    num = 0
    while num < show_this_many:
        p = processes[num]
        pid = str(p.get('pid', 'N/A'))
        name = p.get('name', 'unknown')
        memory = str(p.get('memory', 0))
        
        print(pid + " - " + name + " - " + memory + " MB")
        num = num + 1
    
    print()
    print("Total: " + str(len(processes)) + " processes")
    print()

def save_file(percent, processes, count):
    """Save to file"""
    import time
    
    filename = "report.txt"
    
    try:
        f = open(filename, "w")
        f.write("System Health Report\n")
        f.write("====================\n\n")
        
        f.write("Memory Information:\n")
        f.write("-------------------\n")
        f.write("Used: " + str(percent) + "%\n")
        
        if percent >= 85:
            f.write("Status: BAD\n")
        elif percent >= 75:
            f.write("Status: WARNING\n")
        else:
            f.write("Status: OK\n")
        
        f.write("\n")
        f.write("Top " + str(count) + " Processes:\n")
        f.write("----------------------\n")
        
        # Write processes
        show_this_many = count
        if count > len(processes):
            show_this_many = len(processes)
        
        num = 0
        while num < show_this_many:
            p = processes[num]
            pid = str(p.get('pid', 'N/A'))
            name = p.get('name', 'unknown')
            memory = str(p.get('memory', 0))
            
            f.write(pid + " - " + name + " - " + memory + " MB\n")
            num = num + 1
        
        f.write("\n")
        f.write("Total: " + str(len(processes)) + " processes\n")
        
        f.close()
        print("Saved to " + filename)
        
    except:
        print("Could not save file")

def alert(percent, limit):
    """Simple memory alert"""
    if percent > limit:
        print("\n!!! ALERT !!!")
        print("Memory too high!")
        print(str(percent) + "% > " + str(limit) + "%")
        print()

def main():
    """Test the functions"""
    print("Member 4: Simple Output")
    print()
    
    # Test data
    test_percent = 87.5
    
    test_processes = [
        {'pid': 1234, 'name': 'chrome', 'memory': 512},
        {'pid': 5678, 'name': 'python', 'memory': 256},
        {'pid': 9012, 'name': 'firefox', 'memory': 128}
    ]
    
    # Test memory display
    show_memory(test_percent, 85)
    
    # Test alert
    alert(test_percent, 85)
    
    # Test process display
    show_processes(test_processes, 5)
    
    # Test save
    save_file(test_percent, test_processes, 5)

if __name__ == "__main__":
    main()
