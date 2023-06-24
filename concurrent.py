import os
import argparse
from time import time

from multiprocessing import Process, current_process
from threading import Thread, current_thread
from distutils.util import strtobool
from utils import *

def work_process(sudokus, n_threads, indexes, enable_output):
    threads = []
    for i, sudoku in enumerate(sudokus):
        sudoku_blocks = []
        sudoku_blocks.extend(get_lines(sudoku))
        sudoku_blocks.extend(get_columns(sudoku))
        sudoku_blocks.extend(get_regions(sudoku))
        
        if enable_output:
            print(f"{current_process().name}: resolvendo quebra-cabeças {indexes[i]+1}")

        thread_block = [[] for _ in range(len(sudoku_blocks))]
        [thread_block[j % n_threads].append(blocks) for j, blocks in enumerate(sudoku_blocks)]
        errors = [[] for _ in range(n_threads)]
        for k in range(n_threads):
            thread = Thread(name=f"T{k}", target=work_threads, args=(thread_block[k][:], errors,))
            thread.start()
            threads.append(thread)

        for i, thread in enumerate(threads):
            thread.join()
        
        if enable_output:
            print_concurrent_errors(errors[:], current_process().name)
            

def work_threads(blocks, errors):
    name = current_thread().name
    for block in blocks:
        if set(block[1:]) != {1,2,3,4,5,6,7,8,9}:
            errors[int(name[1:]) - 1].append(block[0])

    aux = [e.replace("L", "A") for e in errors[int(name[1:]) - 1]]
    aux.sort()
    aux = [e.replace("A", "L") for e in aux]
    errors = aux[:]

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
    process_sudokus = [[] for _ in range(args.num_process)]
    [process_sudokus[i % args.num_process].append(sudoku) for i, sudoku in enumerate(sudokus)]
    indexes_sudokus = [[] for _ in range(args.num_process)]
    [indexes_sudokus[i % args.num_process].append(i) for i in range(len(sudokus))]
    # Iniciando os processos
    process = [Process(name=f"Processo {i + 1}", target=work_process, args=(p_s, args.num_threads, indexes_sudokus[i], args.enable_output,)) for i, p_s in enumerate(process_sudokus)]
    for p in process:
        p.start()

    # Esperando terminar os processos
    for p in process:
        p.join()

if __name__ == "__main__":
    start = time()
    concurrent_solution()
    end = time()
    print("Time:", end - start)