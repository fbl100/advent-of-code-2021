import numpy as np

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
    board
    """

    def __init__(self, mx):
        self._matrix = mx
        self._marked = np.zeros(np.shape(mx),dtype=np.bool)

    def mark(self, x):
        """
        >>> b = Board([[1,2], [3,4]])
        >>> b.mark(1)
        False
        >>> b.mark(2)
        True
        """

        rows,cols = np.shape(self._matrix)
        for r in range(0, rows):
            for c in range(0, cols):
                if self._matrix[r][c] == x:
                    self._marked[r][c] = True
                    return is_bingo(self._marked)

        # did not mark anything, wasn't bingo before, it isn't now
        return False







