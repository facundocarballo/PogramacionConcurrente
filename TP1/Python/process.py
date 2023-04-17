import os
import time
from abc import ABC, abstractmethod
from typing import List

PROCESO_A = "A"
PROCESO_B = "B"
PROCESO_C = "C"
PROCESO_D = "D"
PROCESO_E = "E"
PROCESO_F = "F"
PROCESO_G = "G"

class ProcessBase(ABC):
    def __init__(self, name):
        super().__init__()
        self.__name = name
    @abstractmethod
    def execute(self):
        pass
    def print_message(self):
        print("Proceso " + self.__name + " (PID: " + str(os.getpid()) + " | PPID: " + str(os.getppid()) + " )")
    def print_error_message(self):
        print("Error al crear el proceso " + self.__name)

class ProcessLead(ProcessBase):
    def __init__(self, name):
        super().__init__(name)
    def execute(self):
        self.print_message()
        time.sleep(30)
        os._exit(1)
    
class ProcessParent(ProcessBase):
    def __init__(self, name, childs):
        super().__init__(name)
        self.__childs: List[ProcessBase] = childs
    def execute(self):
        self.print_message()
        for child in self.__childs:
            pid = os.fork()
            if (pid == 0):
                child.execute()
            if (pid < 0):
                self.print_error_message()
        time.sleep(30)
        for _ in self.__childs:
            os.wait()
        os._exit(1)

def main():
    process_g = ProcessLead(PROCESO_G)
    process_f = ProcessLead(PROCESO_F)
    process_e = ProcessLead(PROCESO_E)
    process_c = ProcessLead(PROCESO_C)

    process_b = ProcessParent(PROCESO_B, [process_e, process_f])
    process_d = ProcessParent(PROCESO_D, [process_g])
    process_a = ProcessParent(PROCESO_A, [process_b, process_c, process_d])

    process_a.execute()

main()

        

