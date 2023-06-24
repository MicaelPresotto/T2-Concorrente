

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

def print_concurrent_errors(errors, process_name):
    dict_size = sum([len(error) for error in errors])
    msg_error = f"{process_name}: {dict_size} erros encontrados "
    if dict_size:
        aux = []
        for i, error in enumerate(errors):
            if len(error):
                aux.append(f"T{i + 1}: " + ", ".join(error))
        msg_error += "(" + "; ".join(aux) + ")"
    print(msg_error)

def print_serial_errors(errors):
    amount_errors = len(errors)
    msg_error = f"Processo main: {amount_errors} erros encontrados "
    if amount_errors:
        msg_error += "(" + ", ".join(errors) + ")"
    print(msg_error)
