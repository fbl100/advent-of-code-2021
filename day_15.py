import heapq
import sys
import itertools
import more_itertools
from collections import defaultdict, Counter, deque
import re
from queue import PriorityQueue

import numpy as np
from more_itertools import sliding_window
from networkx import Graph


def is_valid(r, c, num_rows, num_cols):
    if r < 0 or c < 0:
        return False
    elif r >= num_rows or c >= num_cols:
        return False

    return True


def neighbor_indices(r, c, num_rows, num_cols):
    all_neghbors = [
        # (r - 1, c - 1),
        (r - 1, c),
        # (r - 1, c + 1),
        (r, c - 1),
        (r, c + 1),
        # (r + 1, c - 1),
        (r + 1, c)
        # (r + 1, c + 1)
    ]

    valid_neighbors = [(r, c) for r, c in all_neghbors if is_valid(r, c, num_rows, num_cols)]
    return valid_neighbors


def parse_line(line):
    '''
    >>> parse_line("123445")
    [1, 2, 3, 4, 4, 5]
    '''
    row = [int(c) for c in line.strip()]
    return row


def load_file(filename) -> np.ndarray:
    with open(filename) as f:
        grid = [parse_line(line) for line in f.readlines()]
    return grid


def print_grid(grid):
    (rows, cols) = np.shape(grid)
    for r in range(0, rows):
        line = "".join([str(grid[r][c]) for c in range(0, cols)])
        print(line)


def cycle_grid(grid):
    '''
    >>> cycle_grid([[1,2],[8,9]])
    array([[2, 3],
           [9, 1]])
    '''

    def f(x):
        return 1 if x == 9 else x + 1

    ret_val = np.vectorize(f)(grid)

    return ret_val


def neighbor(r, c):
    '''
    >>> neighbor(0,0)
    (0, 0)
    >>> neighbor(1,0)
    (0, 0)
    >>> neighbor(1,1)
    (1, 0)
    '''
    if r == 0 and c == 0:
        return (r, c)
    elif c == 0:
        return (r - 1, c)
    else:
        return (r, c - 1)


def inflate_grid(grid, factor):
    '''
    >>> A = np.array([[1,2],[8,9]])
    >>> B = np.array(cycle_grid(A))
    >>> np.block([[A,B],[A,B]])
    array([[1, 2, 2, 3],
           [8, 9, 9, 1],
           [1, 2, 2, 3],
           [8, 9, 9, 1]])
    >>> inflate_grid(A,3)
    array([[1, 2, 2, 3, 3, 4],
           [8, 9, 9, 1, 1, 2],
           [2, 3, 3, 4, 4, 5],
           [9, 1, 1, 2, 2, 3],
           [3, 4, 4, 5, 5, 6],
           [1, 2, 2, 3, 3, 4]])
    '''

    if factor == 1:
        return grid

    g = np.empty((factor, factor), dtype=np.object)
    g[0][0] = np.array(grid)

    for r in range(0, factor):
        for c in range(0, factor):
            if r == 0 and c == 0:
                continue
            (R, C) = neighbor(r, c)
            G = cycle_grid(g[R][C])
            g[r][c] = G

    return np.block(g.tolist())


def process_file(filename, factor):
    grid1 = load_file(filename)

    grid = inflate_grid(grid1, factor)

    print_grid(grid)

    (rows, cols) = np.shape(grid)
    # print(rows)
    # print(cols)

    infinity = int(1E18)
    # print(infinity)

    start = (0, 0)
    end = (rows - 1, cols - 1)

    dist = {
        start: 0
    }

    prev = {}

    Q = PriorityQueue()
    q = []

    for r in range(0, rows):
        for c in range(0, cols):
            v = (r, c)
            if v != start:
                dist[v] = infinity
                prev[v] = None

            q.append((dist[v], v))
            Q.put((dist[v], v))

    heapq.heapify(q)

    while len(q) > 0:
        # print(q)

        (score, u) = q.pop(0)

        for v in neighbor_indices(u[0], u[1], rows, cols):
            risk = grid[v[0]][v[1]]
            alt = dist[u] + risk
            if alt < dist[(v[0], v[1])]:
                dist[v] = alt
                prev[v] = u
                idx = next(i for i, x in enumerate(q) if x[1] == v)
                q[idx] = (alt, v)
            if v == end:
                q.clear()
        heapq.heapify(q)

    path = [end]
    n = end
    sum = grid[n[0]][n[1]]
    while n != start:
        p = prev[n]
        path.append(p)
        if p != start:
            sum += grid[p[0]][p[1]]
        n = p

    print(f"sum = {sum} [{filename}]")

    (rows, cols) = np.shape(grid)
    for r in range(0, rows):
        line = ""
        for c in range(0, cols):
            if (r, c) in path:
                line += str(grid[r][c])
            else:
                line += " "
        print(line)

    #
    # Q.put((4, 'foo'))
    # Q.put((3, 'bar'))
    # Q.put((5, 'baz'))
    #
    # while not Q.empty():
    #     next = Q.get()
    #     print(next)

def reconstruct_path(came_from, current):
    total_path = deque([current])
    while current in came_from:
        current = came_from[current]
        total_path.appendleft(current)
    return list(total_path)


def process_file_astar(filename, factor):
    grid1 = load_file(filename)

    grid = inflate_grid(grid1, factor)

    print_grid(grid)

    (rows, cols) = np.shape(grid)
    # print(rows)
    # print(cols)

    infinity = int(1E18)
    # print(infinity)

    start = (0, 0)
    end = (rows - 1, cols - 1)

    def h(vertex):
        return np.sqrt( (vertex[0] - end[0]) ** 2 + (vertex[1] - end[1]) ** 2)

    gscore = defaultdict(lambda : infinity)
    gscore[start] = 0

    fscore = defaultdict(lambda : infinity)
    fscore[start] = h(start)


    came_from = {}

    openset = []
    openset.append((fscore[start], start))
    heapq.heapify(openset)

    path = None

    while len(openset) > 0 and path is None:
        # print(q)

        (score, current) = openset.pop(0)

        if current == end:
            path = reconstruct_path(came_from, current)
        else:
            for neighbor in neighbor_indices(current[0], current[1], rows, cols):
                tentative_g_score = gscore[current] + grid[neighbor[0]][neighbor[1]]

                if tentative_g_score < gscore[neighbor]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + h(neighbor)
                    if neighbor not in openset:
                        openset.append((fscore[neighbor], neighbor))
            heapq.heapify(openset)

    sum = 0
    for (r,c) in path:
        if r == 0 and c == 0:
            continue
        else:
            sum += grid[r][c]

    print(f"sum = {sum} [{filename}]")

    (rows, cols) = np.shape(grid)
    for r in range(0, rows):
        line = ""
        for c in range(0, cols):
            if (r, c) in path:
                line += str(grid[r][c])
            else:
                line += " "
        print(line)

    #
    # Q.put((4, 'foo'))
    # Q.put((3, 'bar'))
    # Q.put((5, 'baz'))
    #
    # while not Q.empty():
    #     next = Q.get()
    #     print(next)

process_file_astar("day_15_test.txt", 1)
process_file_astar("day_15_test.txt", 5)
#
process_file_astar("day_15_input.txt",1)
process_file_astar("day_15_input.txt",5)
