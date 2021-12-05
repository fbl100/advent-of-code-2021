import numpy as np
import more_itertools

"""
>>> line2array("1 2 3 4 5")
foo
"""


def line2array(line):
    """
    >>> x = line2array("1 2 3 4 5")
    >>> x
    array([1, 2, 3, 4, 5])
    """
    a = np.array(line.split()).astype(np.int)
    return a


def parse_board(lines):
    """
    >>> x = ["1 2 3 4 5", "6 7 8 9 10", "11 12 13 14 15", "16 17 18 19 20", "21 22 23 24 25"]
    >>> parse_board(x)
    [array([1, 2, 3, 4, 5]), array([ 6,  7,  8,  9, 10]), array([11, 12, 13, 14, 15]), array([16, 17, 18, 19, 20]), array([21, 22, 23, 24, 25])]
    """
    retval = [line2array(x) for x in lines]
    return retval


def is_row_bingo(mx, i):
    """
    >>> x = [[False, False, False, False, True], [True, True, True, True, True]]
    >>> is_row_bingo(x, 0)
    False
    >>> is_row_bingo(x, 1)
    True
    """
    is_bingo = True
    for col in range(0, len(mx[i])):
        is_bingo &= mx[i][col]

    return is_bingo


def is_col_bingo(mx, i):
    """
    >>> x = [[False, False, False, False, True], [True, True, True, True, True]]
    >>> is_col_bingo(x, 0)
    False
    >>> is_col_bingo(x, 4)
    True
    """
    is_bingo = True
    for row in range(0, len(mx)):
        is_bingo &= mx[row][i]

    return is_bingo


def is_bingo(mx):
    """
    >>> x = [[False, True], [True, False]]
    >>> is_bingo(x)
    False
    >>> x = [[False, True], [True, True]]
    >>> is_bingo(x)
    True
    """
    shape = np.shape(mx)
    for row in range(0, shape[0]):
        if is_row_bingo(mx, row):
            return True

    for col in range(0, shape[1]):
        if is_col_bingo(mx, col):
            return True

    return False


class Board(object):
    """
    >>> x = parse_board(["1 2 3 4 5", "6 7 8 9 10", "11 12 13 14 15", "16 17 18 19 20", "21 22 23 24 25"])
    >>> board = Board(x)
    >>> board.shape()
    (5, 5)
    """

    def __init__(self, mx):
        self._matrix = mx
        self._marked = np.zeros(np.shape(mx), dtype=np.bool)

    def mark(self, x):
        """
        >>> b = Board([[1,2], [3,4]])
        >>> b.mark(1)
        False
        >>> b.mark(2)
        True
        """

        rows, cols = np.shape(self._matrix)
        for r in range(0, rows):
            for c in range(0, cols):
                if self._matrix[r][c] == x:
                    self._marked[r][c] = True
                    return is_bingo(self._marked)

        # did not mark anything, wasn't bingo before, it isn't now
        return False

    def unmarked(self):

        ret_val = list()
        rows, cols = np.shape(self._matrix)
        for r in range(0, rows):
            for c in range(0, cols):
                if not self._marked[r][c]:
                    ret_val.append(self._matrix[r][c])

        return ret_val

    def shape(self):
        return np.shape(self._matrix)


def process_file(file):
    with open(file) as f:
        lines = f.readlines()

    moves = [int(x) for x in lines[0].split(',')]
    board_lines = lines[2:]

    boards : list[Board] = list()
    working = list()

    def add_board():
        # make a board from the working list
        b = Board(parse_board(working))
        boards.append(b)
        working.clear()

    for l in board_lines:
        if l.strip():
            # we have data
            working.append(l)
        else:
           add_board();

    add_board()

    num_winners = 0
    first_score = 0
    last_score = 0


    for m in moves:
        print(m)
        for b in boards:
            if b.mark(m):
                if len(boards) == 1:
                    x = sum(b.unmarked())
                    last_score = x * m
                    return first_score, last_score
                else:
                    boards.remove(b)
                    if num_winners == 0:
                        x = sum(b.unmarked())
                        first_score = x * m
                    num_winners = num_winners+1
    return first_score,-1

f,l = process_file("day_4_test.txt")
print(f)
print(l)