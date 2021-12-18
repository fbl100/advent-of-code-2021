import sys
import itertools
from collections import defaultdict, Counter, deque
import re


def fold_x(coord, axis):
    '''
    >>> fold_x((8,3), 5)
    (2, 3)
    >>> fold_x((3,3), 5)
    (3, 3)
    '''
    (x, y) = coord
    if x < axis:
        return x, y
    else:
        return axis - (x - axis), y

def fold_y(coord, axis):
    '''
    >>> fold_y((3,8), 5)
    (3, 2)
    >>> fold_y((3,3), 5)
    (3, 3)
    '''
    (x, y) = coord
    if y < axis:
        return x, y
    else:
        return x, axis - (y - axis)

def process_file(filename):
    coords = set()
    folds = []

    regex = re.compile(r"fold along (?P<axis>x|y)=(?P<value>\d+)")
    with open(filename) as f:
        for line in f.readlines():
            if line.strip() == "":
                continue
            m = regex.match(line)
            if m is None:
                # parse as coords
                (x, y) = line.split(",")
                coords.add((int(x), int(y)))
            else:
                axis = m.group('axis')
                value = m.group('value')
                folds.append((axis, int(value)))

    print(coords)
    print(folds)

    current = coords
    for f in folds:
        (axis, value) = f
        nxt = set()
        for c in current:
            if axis == 'x':
                nxt.add(fold_x(c, value))
            else:
                nxt.add(fold_y(c, value))
        current = nxt
        print(f"after fold along {axis} = {value}, length = {len(nxt)}")

    max_x = max(x for x,y in current)
    max_y = max(y for x,y in current)
    print(f"max_x = {max_x}")
    print(f"max_y = {max_y}")

    for y in range(0, max_y+1):
        s = ""
        for x in range(0, max_x+1):
            if (x,y) in current:
                s += "#"
            else:
                s += " "
        print(s)



process_file("day_13_test.txt")
process_file("day_13_input.txt")