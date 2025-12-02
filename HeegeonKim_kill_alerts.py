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

