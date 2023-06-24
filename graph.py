import sys
import time
import matplotlib.pyplot
from concurrent import concurrent_solution
from serial import serial_solution


def get_sample(n_process):
    x = []
    y = []
    MAX_THREAD = 10    
    for n_thread in range(MAX_THREAD):
        start = time.time()
        sys.argv = ["python", "-f", "input-sample.txt", "-p", f"{n_process}", "-t", f"{n_thread}"]
        concurrent_solution()
        end = time.time()
        x.append(n_thread)
        y.append(start - end)
    
    return x, y

def graph():
    pass



if __name__ == "__main__":
    graph()
