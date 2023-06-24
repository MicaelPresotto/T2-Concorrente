import os
import argparse

from distutils.util import strtobool
from utils import *

def worker(sudokus, enable_output):
    erros = [0,0,0,0]
    for i, sudoku in enumerate(sudokus):
        sudoku_blocks = []
        sudoku_blocks.extend(get_lines(sudoku))
        sudoku_blocks.extend(get_columns(sudoku))
        sudoku_blocks.extend(get_regions(sudoku))
        for block in sudoku_blocks:
            if set(block[1:]) != {1,2,3,4,5,6,7,8,9}:
                    erros[i] += 1

    if enable_output:
        for i,j in enumerate(erros):
            print(f"Sudoku {i+1}: {j} erros encontrados")

def valid_file(file):
    if not os.path.exists(file):
        msg = "Valor recebido %s. Arquivo nao existe!" % file
        raise argparse.ArgumentTypeError(msg)
    return file

def serial_solution():
    parser = argparse.ArgumentParser(add_help=True, description='Verificador de Sudoku Concorrente em Python')

    parser.add_argument('-f', '--file-name', action='store', type=valid_file, required=True, help='O nome do arquivo com as solucoes a serem validadas')
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
    
    worker(sudokus, args.enable_output)

if __name__ == "__main__":
    serial_solution()