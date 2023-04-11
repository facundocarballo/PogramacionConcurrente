
import os
import sys
import time

def print_process_message(char_of_process):
    print("Soy el proceso " + char_of_process + " ( PID: " + str(os.getpid()) + " | PPID: " + str(os.getppid()) + " )")

	
def parent():

    print_process_message('A')
    pidB = os.fork()

    if pidB == 0:
        pidB = os.getpid()
        print_process_message('B')
        pidE = os.fork()
        if pidE == 0:
            pidE = os.getpid()
            print_process_message('E')
            time.sleep(30)
            exit(0)
        
        pidF = os.fork()
        if pidF == 0:
            pidF = os.getpid()
            print_process_message('F')
            time.sleep(30)
            exit(0)
        
        time.sleep(30)
        exit(0)
    
    pidC = os.fork()
    if pidC == 0:
        pidC = os.getpid()
        print_process_message('C')
        time.sleep(30)
        exit(0)
    
    pidD = os.fork()
    if pidD == 0:
        pidD = os.getpid()
        print_process_message('D')
        pidG = os.fork()
        if pidG == 0:
            pidG = os.getpid()
            print_process_message('G')
            time.sleep(30)
            exit(0)
        
        time.sleep(30)
        exit(0)
    
    time.sleep(30)
    return 0
    
    

parent()