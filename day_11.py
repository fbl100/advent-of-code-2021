import numpy as np

def is_valid(r, c, num_rows, num_cols):
    if r < 0 or c < 0:
        return False
    elif r >= num_rows or c >= num_cols:
        return False

    return True


def neighbor_indices(r, c, num_rows, num_cols):
    all_neghbors = [
        (r - 1, c - 1),
        (r - 1, c),
        (r - 1, c + 1),
        (r, c - 1),
        (r, c + 1),
        (r + 1, c - 1),
        (r + 1, c),
        (r + 1, c + 1)
    ]

    valid_neighbors = [(r, c) for r, c in all_neghbors if is_valid(r, c, num_rows, num_cols)]
    return valid_neighbors


def increment(board: np.ndarray):
    """
    >>> board = np.array([[1,2],[3,4]])
    >>> increment(board)
    >>> board
    array([[2, 3],
           [4, 5]])
    """
    board += 1


def flash_cell(board, flashed, row, col):
    """
    >>> board = np.array([[1,1,1,1,1], [1,9,9,9,1], [1,9,1,9,1], [1,9,9,9,1], [1,1,1,1,1]])
    >>> flashed = np.zeros(shape=(5,5),dtype=bool)
    >>> increment(board)
    >>> board
    array([[ 2,  2,  2,  2,  2],
           [ 2, 10, 10, 10,  2],
           [ 2, 10,  2, 10,  2],
           [ 2, 10, 10, 10,  2],
           [ 2,  2,  2,  2,  2]])
    >>> count = flash_cell(board, flashed,1,1)
    >>> board
    array([[ 3,  4,  5,  4,  3],
           [ 4, 13, 15, 13,  4],
           [ 5, 15, 10, 15,  5],
           [ 4, 13, 15, 13,  4],
           [ 3,  4,  5,  4,  3]])
    >>> count
    9
    """

    num_rows, num_cols = np.shape(board)
    ret_val = 1 # for this cell
    flashed[row][col] = True # this cell has flashed
    neighbors = neighbor_indices(row, col, num_rows, num_cols)
    for r,c in neighbors:
        board[r][c] += 1
        if flashed[r][c] == False and board[r][c] >= 10:
            ret_val += flash_cell(board,flashed,r,c)

    return ret_val



def step(board):
    """
    >>> board = np.array([[1,1,1,1,1], [1,9,9,9,1], [1,9,1,9,1], [1,9,9,9,1], [1,1,1,1,1]])
    >>> count = step(board)
    >>> count
    9
    >>> board
    array([[3, 4, 5, 4, 3],
           [4, 0, 0, 0, 4],
           [5, 0, 0, 0, 5],
           [4, 0, 0, 0, 4],
           [3, 4, 5, 4, 3]])
    >>> count = step(board)
    >>> count
    0
    >>> board
    array([[4, 5, 6, 5, 4],
           [5, 1, 1, 1, 5],
           [6, 1, 1, 1, 6],
           [5, 1, 1, 1, 5],
           [4, 5, 6, 5, 4]])
    """
    flashed = np.zeros(shape=np.shape(board), dtype=bool)
    num_rows, num_cols = np.shape(board)
    increment(board)
   # print_board(board, "after increment")

    for r in range(0,num_rows):
        for c in range(0, num_cols):
            if not flashed[r][c] and board[r][c] == 10:
                flash_cell(board,flashed,r,c)

    sum = 0
    for r in range(0,num_rows):
        for c in range(0, num_cols):
            if flashed[r][c]:
                board[r][c] = 0
                sum += 1

    return sum

def process_line(line):
    """
    >>> process_line("5483143223")
    [5, 4, 8, 3, 1, 4, 3, 2, 2, 3]
    """
    return [int(x) for x in line.strip()]

def int2char(x):
    if x == 0:
        return '\033[1m' + str(x) + '\033[0m'
    elif x < 10:
        return str(x)
    else:
        return "x"

def print_board(board, text):
    print(text)
    for row in range(0,len(board)):
        chars = [int2char(c) for c in board[row]]
        line = "".join(chars)
        print(line)
    print()


def process_file(file, iterations, break_on_all_flash = False):

    with open(file) as f:
        board = [process_line(line) for line in f.readlines()]

    board = np.array(board)

    num_rows, num_cols = np.shape(board)
    sum = 0
    # print_board(board, "Before any steps: 0")

    iteration_count = 0
    for i in range(0,iterations):
        count = step(board)
        iteration_count += 1
        if count == num_rows * num_cols and break_on_all_flash:
            print(f"All flashed on iteration {iteration_count}")
            break
        sum += count
        # print_board(board, f"After step {i+1} ({sum} flashes)")

    print_board(board, f"After step {iteration_count} ({sum} flashes)")

process_file("day_11_test.txt", 1000, True)
process_file("day_11_input.txt", 1000, True)