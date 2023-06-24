import sys
import time
import matplotlib.pyplot
from concurrent import concurrent_solution
from serial import serial_solution


def get_sample(n_process):
    x = []
    y = []
    MAX_THREAD = 10    
    for n_thread in range(1, MAX_THREAD + 1):
        start = time.time()
        sys.argv = ["python", "-f", "input-sample.txt", "-p", f"{n_process}", "-t", f"{n_thread}", "-e", "False"]
        concurrent_solution()
        end = time.time()
        x.append(n_thread)
        y.append(end - start)
    
    return x[:], y[:]

def graph():
    x, y = get_sample(10)
    matplotlib.pyplot.plot(x, y)
    matplotlib.pyplot.show()



if __name__ == "__main__":
    graph()
