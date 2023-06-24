import os
import sys
import time
import argparse

from multiprocessing import Process
from threading import Thread

def get_lines(sudoku):
    return sudoku[:]

def get_columns(sudoku):
    return [[sudoku[l][c] for l in range(len(sudoku))] for c in range(len(sudoku))]

def get_regions(sudoku):
    regions = [[] for _ in range(9)]
    for r in range(9):
        for l in range((r // 3) * 3, (r // 3) * 3 + 3):
            for c in range((r % 3) * 3, (r % 3) * 3 + 3):
                regions[r].append(sudoku[l][c])
    return regions[:]

def work_process(sudokus, n_threads):
    threads = []
    for i, sudoku in enumerate(sudokus):
        sudoku_blocks = []
        sudoku_blocks.extend(get_lines(sudoku))
        sudoku_blocks.extend(get_columns(sudoku))
        sudoku_blocks.extend(get_regions(sudoku))
        q = 27 // n_threads
        r = 27 % n_threads
        begin = 0
        end = q
        for _ in range(n_threads):
            if r:
                end+=1
                r-=1
            thread = Thread(target=work_threads, args=(sudoku_blocks[begin:end],))
            thread.start()
            threads.append(thread)
            begin = end
            end += q
        for thread in threads:
            thread.join()

def work_threads(blocks):
    for block in blocks:
        if set(block) != {1,2,3,4,5,6,7,8,9}:
            pass

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

def main():
    # Definindo os parametros do programa
    parser = argparse.ArgumentParser(add_help=True, description='Verificador de Sudoku Concorrente em Python')

    parser.add_argument('-f', '--file-name', action='store', type=valid_file, required=True, help='O nome do arquivo com as solucoes a serem validadas')
    parser.add_argument('-p', '--num-process', action='store', type=pos_int, required=True, help='O numero de processos trabalhadores')
    parser.add_argument('-t', '--num-threads', action='store', type=pos_int, required=True, help='O numero de threads de correcao a serem utilizadas por cada processo trabalhador')

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

    # Fazendo a divisao de trabalho das threads
    process_sudokus = [[] for _ in range(args.num_process)]
    [process_sudokus[i % args.num_process].append(sudoku) for i, sudoku in enumerate(sudokus)]

    # Iniciando os processos
    process = [Process(target=work_process, args=(p_s, args.num_threads)) for p_s in process_sudokus]
    for p in process:
        p.start()

    # Esperando terminar os processos
    for p in process:
        p.join()

def make_graph():
    pass

if __name__ == '__main__':
    for n_process in range(1, 10):
        for n_thread in range(1, 10):
            sys.argv = ["python3", 
                        "-p", f"{n_process}",
                        "-t", f"{n_thread}",
                        "-f", "input-sample.txt"]
            inicio = time.time()
            main()
            fim = time.time()
            print(fim - inicio)