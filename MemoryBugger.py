#!/usr/bin/env python3

# Author: Mikal Dixon

"""Prevents no memory error, AttributeError"""
def main():
    global ALERT_THRESHOLD
    while True:
        clear_screen()
        processes = sorted(
            psutil.process_iter(['pid', 'name', 'memory_info', 'exe']),
            key=lambda p: p.info['memory_info'].rss if p.info['memory_info'] else 0,
            reverse=True
        )
        top_proc_data = None
        if processes:
            top_proc_data = {
                'pid': processes[0].info['pid'],
                'name': processes[0].info['name'],
                'proc_obj': processes[0]
            }