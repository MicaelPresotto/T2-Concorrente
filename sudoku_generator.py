import random

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
    sudokus = []
    states = [[[0 for i in range(9)] for j in range(9)]]

    possibilities = [[get_possible_numbers(states[-1], l, c) for c in range(9)] for l in range(9)]
    while True:
        spaces = get_empty_spaces(states[-1])
        if len(spaces) == 0:
            if n_sudokus == len(sudokus):
                break
            else:
                sudokus.append([[e for e in l] for l in states[-1]])
                states.pop(-1)
                break

        line, column = spaces[0]
        if len(possibilities[line][column]) == 0:
            states.pop(-1)
            continue
        
        number = random.choice(possibilities[line][column])
        states.append([[e for e in l] for l in states[-1]])
        states[-1][line][column] = number
        possibilities[line][column].remove(number)

    return states[-1]

if __name__=="__main__":
    for line in generate_sudokus(1):
        for e in line:
            print(e, end="")
        print()