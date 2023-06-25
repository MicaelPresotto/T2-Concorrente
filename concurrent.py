import argparse

from multiprocessing import Process, current_process
from threading import Thread, current_thread
from distutils.util import strtobool
from utils import *


def work_process(sudokus, n_threads, shift, enable_output):
    threads = []

    for i, sudoku in enumerate(sudokus):
        
        if enable_output:
            print(f"{current_process().name}: resolvendo quebra-cabeças {i + shift + 1}")
    
        blocks = []
        blocks.extend(get_rows(sudoku))
        blocks.extend(get_columns(sudoku))
        blocks.extend(get_regions(sudoku))

        q = 27 // n_threads
        r = 27 % n_threads
        start = 0
        errors = [[] for _ in range(n_threads)]
        for k in range(n_threads):
            amount_blocks = q
            if r:
                r -= 1
                amount_blocks += 1
            thread = Thread(name=f"T{k + 1}", target=work_threads, args=(blocks[start:start+amount_blocks], errors[k]))
            thread.start()
            threads.append(thread)
            start += amount_blocks

        for i, thread in enumerate(threads):
            thread.join()

        if enable_output:
            print_concurrent_errors(errors, current_process().name)

def work_threads(blocks, errors):
    index = int(current_thread().name[1:])
    for block in blocks:
        if set(block[1:]) != {1,2,3,4,5,6,7,8,9}:
            errors.append(block[0])
    aux = [e.replace("L", "A") for e in errors]
    aux.sort()
    aux = [e.replace("A", "L") for e in aux]
    errors = aux[:]

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
        amount_sudokus = q
        if r:
            r -= 1
            amount_sudokus += 1
        p = Process(name=f"Processo {i + 1}", target=work_process, args=(sudokus[start:start+amount_sudokus], args.num_threads, start, args.enable_output,))
        p.start()
        process.append(p)
        start += amount_sudokus

    for p in process:
        p.join()

if __name__ == "__main__":
    concurrent_solution()