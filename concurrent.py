import os
import argparse
from time import time

from multiprocessing import Process, current_process
from threading import Thread, current_thread, Lock
from distutils.util import strtobool
from utils import *

dones = 0
start = 0

def get_errors(blocks):
    pass

def work_process(sudokus, n_threads, shift, enable_output):
    threads = []
    blocks_per_sudokus = [[] for _ in sudokus]
    blocks_per_sudokus_per_thread = [[[] for __ in range(n_threads)] for _ in sudokus]

    for i, sudoku in enumerate(sudokus):
        blocks_per_sudokus[i].extend(get_rows(sudoku))
        blocks_per_sudokus[i].extend(get_columns(sudoku))
        blocks_per_sudokus[i].extend(get_regions(sudoku))

        q = 27 // n_threads
        r = 27 % n_threads
        start = 0
        for k in range(n_threads):
            amount_sudokus = q
            if r:
                r -= 1
                amount_sudokus += 1
            blocks_per_sudokus_per_thread[i][k] = blocks_per_sudokus[i][start:start+amount_sudokus]
            start += amount_sudokus

    locks = [Lock() for _ in range(n_threads)]
    lock_dones = Lock()
    lock_start = Lock()
    errors = [[] for _ in range(n_threads)]
    for k in range(n_threads):
        thread = Thread(name=f"T{k + 1}", target=work_threads, args=([blocks_per_sudokus_per_thread[i][k] for i in range(len(sudokus))], shift, enable_output, locks, lock_dones, lock_start, errors))
        thread.start()
        threads.append(thread)

    for i, thread in enumerate(threads):
        thread.join()

def work_threads(blocks_per_sudoku, shift, enable_output, locks, lock_done, lock_start, errors):
    global start
    global dones
    for i, blocks in enumerate(blocks_per_sudoku):

        if enable_output:
            with lock_start:
                if start == 0:
                    print(f"{current_process().name}: resolvendo quebra-cabeças {i + shift + 1}")
                start += 1
        locks[int(current_thread().name[1:]) - 1].acquire()

        for block in blocks:
            if set(block[1:]) != {1,2,3,4,5,6,7,8,9}:
                errors[int(current_thread().name[1:]) - 1].append(block[0])
        aux = [e.replace("L", "A") for e in errors[int(current_thread().name[1:]) - 1]]
        aux.sort()
        aux = [e.replace("A", "L") for e in aux]
        errors[int(current_thread().name[1:]) - 1] = aux[:]

        with lock_done:
            dones += 1
            if dones == len(locks):
                if enable_output:
                    print_concurrent_errors(errors, current_process().name)
                for lock in locks:
                    lock.release()
                for error in errors:
                    error.clear()
                dones = 0
                start = 0

def pos_int(value):
    pos_i = int(value)
    if pos_i < 1:
        msg = "Valor recebido %s. Tente um valor > 0!" % value
        raise argparse.ArgumentTypeError(msg)
    return pos_i

def valid_file(file):
    if not os.path.exists(file):
        msg = "Valor recebido %s. Arquivo nao existe!" % file
        raise argparse.ArgumentTypeError(msg)
    return file

def concurrent_solution():
    # Definindo os parametros do programa
    parser = argparse.ArgumentParser(add_help=True, description='Verificador de Sudoku Concorrente em Python')

    parser.add_argument('-f', '--file-name', action='store', type=valid_file, required=True, help='O nome do arquivo com as solucoes a serem validadas')
    parser.add_argument('-p', '--num-process', action='store', type=pos_int, required=True, help='O numero de processos trabalhadores')
    parser.add_argument('-t', '--num-threads', action='store', type=pos_int, required=True, help='O numero de threads de correcao a serem utilizadas por cada processo trabalhador')
    parser.add_argument('-e', '--enable_output', action="store", type=lambda x:bool(strtobool(x)), required=False, default=True,  help='Ativa oudesativa so prints')
    # Tratando eventuais erros de entrada
    try:
        args = parser.parse_args()
    except Exception as e:
        print(e)
        exit(1)

    # Lendo as matrizes de sudokus
    sudokus = []
    with open(args.file_name) as file:
        sudokus = [[[int(e) for e in line] for line in sudoku.split("\n")] for sudoku in file.read().split("\n\n")]
       
    if args.num_process > len(sudokus):
        args.num_process = len(sudokus)

    # Fazendo a divisao de trabalho das threads
    process = []
    q = len(sudokus) // args.num_process
    r = len(sudokus) % args.num_process
    start = 0
    for i in range(args.num_process):
        print(i)
        amount_sudokus = q
        if r:
            r -= 1
            amount_sudokus += 1
        p = Process(name=f"Processo {i + 1}", target=work_process, args=(sudokus[start:start+amount_sudokus], args.num_threads, start, args.enable_output,))
        p.start()
        start += amount_sudokus
        process.append(p)

    for p in process:
        p.join()

if __name__ == "__main__":
    start = time()
    concurrent_solution()
    end = time()
    print("Time:", end - start)