import psutil
import time
import os
import sys

# Set alert threshold (default 80%)
ALERT_THRESHOLD = 80

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_size(bytes, suffix="B"):
    """
    Convert bytes to a human-readable format (e.g., 10MB, 1GB)
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def get_process_details(pid):
    """
    Get detailed path and command info for a single PID
    """
    try:
        p = psutil.Process(pid)
        return {
            'name': p.name(),
            'exe': p.exe(),            # Absolute path to the executable
            'cmdline': " ".join(p.cmdline()),  # Full command line arguments
            'cwd': p.cwd(),            # Current working directory
            'status': p.status(),
            'memory': get_size(p.memory_info().rss)
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

def show_overall_memory(top_process=None):
    svmem = psutil.virtual_memory()
    print("="*70)
    print(f"[ System Memory Status ]")
    print(f"Total: {get_size(svmem.total)} | Available: {get_size(svmem.available)}")
    print(f"Used:  {get_size(svmem.used)} ({svmem.percent}%)")
    
    # Alert Logic
    if svmem.percent > ALERT_THRESHOLD:
        print(f"\n[!] ALERT: Memory usage ({svmem.percent}%) exceeds threshold! [!]")
        if top_process:
            print(f">>> Top Consumer: [{top_process['name']}] (PID: {top_process['pid']})")
            # Try to get path; show warning if permission denied
            try:
                p_path = top_process['proc_obj'].exe()
                print(f"    Path: {p_path}")
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                print(f"    Path: (Permission Denied - cannot read path)")
    else:
        print(f"\nStatus: Normal (Threshold: {ALERT_THRESHOLD}%)")
    print("="*70)

def inspect_process():
    """
    Function to inspect a specific PID in detail
    """
    pid_input = input("\n[?] Enter PID to inspect (0 to return): ")
    if pid_input == '0': return

    try:
        pid = int(pid_input)
        details = get_process_details(pid)
        
        if details:
            print("\n" + "*"*70)
            print(f"PID:    {pid}")
            print(f"Name:   {details['name']}")
            print(f"Memory: {details['memory']}")
            print(f"Status: {details['status']}")
            print("-" * 70)
            print(f"[Executable Path]: \n   {details['exe']}")
            print("-" * 70)
            print(f"[Full Command]: \n   {details['cmdline']}")
            print("-" * 70)
            print(f"[Working Directory]: \n   {details['cwd']}")
            print("*"*70)
        else:
            print("[Error] Cannot read PID info (Permission denied or process ended).")

    except ValueError:
        print("[Error] Please enter a valid numeric PID.")
    except Exception as e:
        print(f"Error: {e}")
    
    input("\nPress Enter to return...")

def kill_process():
    pid_input = input("\n[!] Enter PID to KILL (0 to return): ")
    if pid_input == '0': return

    try:
        pid = int(pid_input)
        p = psutil.Process(pid)
        print(f"Locking on: {p.name()} ({get_size(p.memory_info().rss)})")
        confirm = input(f"[!] Are you sure you want to force kill PID {pid}? (y/n): ")
        
        if confirm.lower() == 'y':
            p.kill() # Using kill() for immediate termination
            print(f"[OK] PID {pid} has been killed.")
            time.sleep(1)
        else:
            print("Operation cancelled.")
            
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        print(f"[Error] Failed to kill process: {e} (Try running with sudo)")
    except ValueError:
        print("[Error] Please enter a valid number.")
    
    input("Press Enter to continue...")

def main():
    global ALERT_THRESHOLD
    while True:
        clear_screen()
        
        # Gather process data first
        processes = sorted(
            [p for p in psutil.process_iter(['pid', 'name', 'memory_info', 'exe'])],
            key=lambda p: p.info['memory_info'].rss, 
            reverse=True
        )
        
        top_proc_data = None
        if processes:
            top_proc_data = {
                'pid': processes[0].info['pid'],
                'name': processes[0].info['name'],
                'proc_obj': processes[0]
            }

        show_overall_memory(top_proc_data)
        
        # Display Process List
        print(f"\n[ Top 10 Memory Processes ]")
        print(f"{'PID':<8} {'Memory':<10} {'Name':<20} {'File Path (Partial)'}")
        print("-" * 70)
        for p in processes[:10]:
            pid = p.info['pid']
            mem = get_size(p.info['memory_info'].rss)
            name = p.info['name']
            try:
                path = p.info['exe'] if p.info['exe'] else "[System Process]"
            except:
                path = "[Permission Denied]"
            
            # Truncate path if too long
            display_path = (path[:30] + '..') if len(path) > 30 else path
            print(f"{pid:<8} {mem:<10} {name:<20} {display_path}")
        print("-" * 70)

        print("\n[ Options ]")
        print("1. Refresh")
        print("2. Inspect Detail & Path")
        print("3. Kill Process")
        print("4. Set Alert Threshold")
        print("5. Exit")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1': continue
        elif choice == '2': inspect_process()
        elif choice == '3': kill_process()
        elif choice == '4':
            try:
                ALERT_THRESHOLD = int(input("Enter new threshold (1-100): "))
            except: pass
        elif choice == '5': sys.exit()

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("[NOTE] Run with 'sudo' to see all system paths and kill processes.")
        time.sleep(2)
    main()
