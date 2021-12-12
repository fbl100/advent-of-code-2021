import re
from collections import Counter
from functools import reduce
import networkx as nx
import numpy as np
from networkx import node_connectivity, dfs_edges, dfs_successors, dfs_postorder_nodes


def parse_line(line):
    """
    >>> parse_line("2199943210")
    [2, 1, 9, 9, 9, 4, 3, 2, 1, 0]
    """
    return [int(c) for c in line.strip()]


def is_valid(r,c, num_rows, num_cols):
    if r < 0 or c < 0:
        return False
    elif r >= num_rows or c >= num_cols:
        return False

    return True

def neighbor_indices(r, c, num_rows, num_cols):
    all_neghbors = [
        (r - 1, c),
        (r, c - 1),
        (r + 1, c),
        (r, c + 1)
    ]

    valid_neighbors = [(r,c) for r,c in all_neghbors if is_valid(r,c,num_rows,num_cols)]
    return valid_neighbors

def get_id(r,c,num_cols):
    return r*num_cols + c

def process_file_risk_level(filename):
    with open(filename) as f:
        lines = [parse_line(x) for x in f.readlines()]

    rows = len(lines)
    cols = len(lines[0])

    risk_level = 0
    for r in range(0, rows):
        for c in range(0, cols):
            x = lines[r][c]
            ni = neighbor_indices(r,c,rows,cols)
            neighbors = [lines[row][col] for row,col in ni]
            count = len([n for n in neighbors if n > x])

            if count == len(ni):
                risk_level += (x+1)
            # print(f"[{r},{c}] - [{count == len(ni)}] {x} {neighbors}")

    print(f"risk level: {risk_level}")


def find_low_points(mx):

    rows = len(mx)
    cols = len(mx[0])

    for r in range(0, rows):
        for c in range(0, cols):
            x = mx[r][c]
            ni = neighbor_indices(r,c,rows,cols)
            neighbors = [mx[row][col] for row,col in ni]
            count = len([n for n in neighbors if n > x])

            if count == len(ni):
                yield get_id(r,c,cols)


def process_file_bfs(filename):
    with open(filename) as f:
        lines = [parse_line(x) for x in f.readlines()]

    rows = len(lines)
    cols = len(lines[0])


    G = nx.Graph()
    for r in range(0, rows):
        for c in range(0, cols):
            id = get_id(r,c,cols)
            val = lines[r][c]
            if val != 9:
                G.add_node(id, value=val)

    for r in range(0, rows):
        for c in range(0, cols):
            ni = neighbor_indices(r, c, rows, cols)

            id = get_id(r,c,cols)
            if id in G.nodes:
                n_ids = [n for n in [get_id(nr,nc, cols) for nr,nc in ni] if n in G.nodes]
                G.add_edges_from([(id,n) for n in n_ids])

    pts = list(find_low_points(lines))

    basin_sizes = sorted([len(list(dfs_postorder_nodes(G,pt))) for pt in pts])
    vals = basin_sizes[-3:]
    print(f"product: {np.prod((vals))}")


process_file_risk_level('day_9_test.txt')
process_file_risk_level('day_9_input.txt')
process_file_bfs('day_9_test.txt')
process_file_bfs('day_9_input.txt')
