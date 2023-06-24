import os
import argparse

from multiprocessing import Process, current_process
from threading import Thread, current_thread

def get_lines(sudoku):
    return [[f"L{i + 1}", *line] for i, line in enumerate(sudoku)]

def get_columns(sudoku):
    t = [[sudoku[l][c] for l in range(9)] for c in range(9)]
    return [[f"C{i + 1}", *col] for i, col in enumerate(t)]

def get_regions(sudoku):
    regions = [[f"R{i + 1}", ] for i in range(9)]
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
        
        print(f"{current_process().name}: resolvendo quebra-cabeças {i + 1}")
        thread_block = [[] for _ in range(len(sudoku_blocks))]
        [thread_block[j % n_threads].append(blocks) for j, blocks in enumerate(sudoku_blocks)]
        errors = {}
        for k in range(n_threads):
            thread = Thread(name=f"T{k}", target=work_threads, args=(thread_block[k][:], errors,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        
        dict_size = sum([len(errors[k]) for k in errors.keys()])
        msg_error = f"{current_process().name}: {dict_size} erros encontrados "
        if dict_size:
            msg_error += "(" + "; ".join([t + ": " + ", ".join(errors[t]) for t in errors.keys()]) + ")"
        print(msg_error)

def work_threads(blocks, errors):
    name = current_thread().name
    errors[name] = []
    for block in blocks:
        if set(block[1:]) != {1,2,3,4,5,6,7,8,9}:
            errors[name].append(block[0])

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
    process = [Process(name=f"Processo {i + 1}", target=work_process, args=(p_s, args.num_threads)) for i, p_s in enumerate(process_sudokus)]
    for p in process:
        p.start()

    # Esperando terminar os processos
    for p in process:
        p.join()

if __name__ == "__main__":
    main()