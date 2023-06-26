import sys

from multiprocessing import Process, current_process
from threading import Thread
from utils import *


def work_process(sudokus, n_threads, shift, enable_output):
    threads = []

    for i, sudoku in enumerate(sudokus):
        if enable_output:
            print(f"{current_process().name}: resolvendo quebra-cabeças {i + shift + 1}")
    
        errors = [[] for _ in range(n_threads)]
        jobs = divide_jobs(get_blocks(sudoku), n_threads)
        for k in range(n_threads):
            threads.append(Thread(name=f"T{k + 1}", target=work_threads, args=(jobs[k], errors[k])))
            threads[-1].start()

        for i, thread in enumerate(threads):
            thread.join()

        if enable_output:
            print_concurrent_errors(errors, current_process().name)

def work_threads(blocks, errors):
    [errors.append(e.replace("A", "L")) for e in sorted([e.replace("L", "A") for e in get_errors(blocks)])]

def concurrent_solution_v1():
    # Definindo os parametros do programa
    try:
        if len(sys.argv) < 5:
                raise IndexError("Passou menos argumentos do que esperado!")
        elif len(sys.argv) > 5:
            raise IndexError("Passou mais argumentos do que esperado")
        file_name = valid_file(sys.argv[1])
        num_process = pos_int(sys.argv[2])
        num_threads = pos_int(sys.argv[3])
        enable_output = valid_bool(sys.argv[4])
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
    concurrent_solution_v1()