

def get_possible_numbers(sudoku, line, column):
    possible_numbers = [i for i in range(1, 10)]

    s_r_y = line // 3
    s_r_x = column // 3
    e_r_y = s_r_y + 3
    e_r_x = s_r_x + 3
    for i in range(9):
        if possible_numbers.count(sudoku[line][i]):
            possible_numbers.remove(sudoku[line][i])
        if possible_numbers.count(sudoku[i][column]):
            possible_numbers.remove(sudoku[i][column])


    for x in range(s_r_x, e_r_x):
        for y in range(e_r_y, e_r_y):
            if possible_numbers.count(sudoku[y][x]):
                possible_numbers.remove(sudoku[y][x])

    return possible_numbers[:]

def get_empty_spaces(sudoku):
    positions = []
    for line, l in enumerate(sudoku):
        for column, v in enumerate(l):
            if not v:
                positions.append((line, column))
    return positions[:]

def generate_sudokus(n_sudokus):
    sudoku = [[0 for __ in range(9)] for _ in range(9)]
    states = [[get_possible_numbers(sudoku, line, column) for column in range(9)] for line in range(9)]

    for _ in range(n_sudokus):
        while len(get_empty_spaces(sudoku)) != 0:
            


if __name__=="__main__":
    generate_sudokus(1)