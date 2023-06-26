import sys

from multiprocessing import Process, current_process
from threading import Thread, current_thread, Lock
from utils import *

dones = 0
start = 0

def work_process(sudokus, n_threads, shift, enable_output):
    blocks_per_sudokus_per_thread = [[[] for __ in range(n_threads)] for _ in sudokus]
    for i, sudoku in enumerate(sudokus):
        for k, job in enumerate(divide_jobs(get_blocks(sudoku), n_threads)):
            blocks_per_sudokus_per_thread[i][k] = job

    threads = []
    locks = [Lock() for _ in range(n_threads)]
    lock_dones = Lock()
    lock_start = Lock()
    errors = [[] for _ in range(n_threads)]
    for k in range(n_threads):
        threads.append(Thread(name=f"T{k + 1}", target=work_threads, args=([blocks_per_sudokus_per_thread[i][k] for i in range(len(sudokus))], shift, enable_output, locks, lock_dones, lock_start, errors)))
        threads[-1].start()

    for i, thread in enumerate(threads):
        thread.join()

def work_threads(blocks_per_sudoku, shift, enable_output, locks, lock_done, lock_start, errors):
    global start
    global dones
    for i, blocks in enumerate(blocks_per_sudoku):
        locks[int(current_thread().name[1:]) - 1].acquire()
        if enable_output:
            with lock_start:
                if start == 0:
                    print(f"{current_process().name}: resolvendo quebra-cabeças {i + shift + 1}")
                start += 1
    
        errors[int(current_thread().name[1:]) - 1] = [e.replace("A", "L") for e in sorted([e.replace("L", "A") for e in get_errors(blocks)])]

        with lock_done:
            dones += 1
            if dones == len(locks):
                dones = 0
                with lock_start:
                    start = 0
                if enable_output:
                    print_concurrent_errors(errors, current_process().name)
                for error in errors:
                    error.clear()
                for lock in locks:
                    lock.release()

def concurrent_solution_v2():
    # Definindo os parametros do programa
    try:
        if len(sys.argv) < 4:
                raise IndexError("Passou menos argumentos do que esperado!")
        elif len(sys.argv) > 5:
            raise IndexError("Passou mais argumentos do que esperado")
        file_name = valid_file(sys.argv[1])
        num_process = pos_int(sys.argv[2])
        num_threads = pos_int(sys.argv[3])
        enable_output = True if len(sys.argv) == 4 else valid_bool(sys.argv[4])
    except IndexError as e:
        print(e)
        sys.exit()

    sudokus = read_sudokus(file_name)

    if num_process > len(sudokus):
        num_process = len(sudokus)

    # Fazendo a divisao de trabalho das threads
    process = []
    jobs = divide_jobs(sudokus, num_process)
    for i in range(num_process):
        process.append(Process(name=f"Processo {i + 1}", target=work_process, args=(jobs[i], num_threads, sum([len(job) for job in jobs[:i]]), enable_output,)))
        process[-1].start()

    for p in process:
        p.join()

if __name__ == "__main__":
    concurrent_solution_v2()