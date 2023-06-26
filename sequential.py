import sys
from distutils.util import strtobool
from utils import *

def worker(sudokus, enable_output):
    for i, sudoku in enumerate(sudokus):
        
        if enable_output:
            print(f"Processo main: resolvendo quebra-cabeças {i}")

        errors = get_errors(get_blocks(sudoku))

        if enable_output:
            print_serial_errors(errors[:])

def sequential_solution():
    try:
        if len(sys.argv) < 2:
                raise IndexError("Passou menos argumentos do que esperado!")
        elif len(sys.argv) > 3:
            raise IndexError("Passou mais argumentos do que esperado")
        file_name = valid_file(sys.argv[1])
        enable_output = True if len(sys.argv) == 2 else valid_bool(sys.argv[2])
    except IndexError as e:
        print(e)
        sys.exit()

    sudokus = read_sudokus(file_name)
    
    worker(sudokus, enable_output)

if __name__ == "__main__":
    sequential_solution()