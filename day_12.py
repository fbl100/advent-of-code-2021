import networkx as nx
from networkx import Graph
from collections import deque, Counter


def build_graph(file_name):
    '''
    >>> str(build_graph('day_12_test_1.txt'))
    'Graph with 6 nodes and 7 edges'
    '''
    G = Graph()
    with open(file_name) as f:
        for line in f.readlines():
            a,b = line.strip().split('-')
            G.add_edge(a,b)
    return G

def part_1():
    '''
    >>> q = deque()
    >>> q.append(1)
    >>> q.append(2)
    >>> q.append(3)
    >>> str(q)
    'deque([1, 2, 3])'
    >>> q.popleft()
    1
    >>> str(q)
    'deque([2, 3])'
    '''
    G = build_graph('day_12_test_1.txt')

    nodes = set(G.nodes)
    edges = list(G.neighbors('start'))

    q = deque()
    explored_large = set()
    explored_small = set()

    def enqueue(x):
        q.append(x)

    def dequeue():
        return q.popleft()

    def explore(n : str):
        if n.isupper():
            explored_large.add(n)
        else:
            explored_small.add(n)


    explore('start')
    enqueue('start')
    while not len(q) == 0:
        v = dequeue()
        if v == 'end':
            print("end")

        for n in G.neighbors(v):
            if n.isupper() or n not in explored_small:
                print(f"exploring {n}")
                explore(n)
                enqueue(n)



def solve_with_loops(filename):
    G = build_graph(filename)

    completed_routes = []
    routes = []
    routes.append(['start'])

    while len(routes) > 0:
        new_routes = []
        for r in routes:
            # new_routes = []
            last_node = r[-1]
            if last_node == 'end':
                # route is complete, add it to completed routes
                completed_routes.append(r)
                # print(f"completed {str(r)}")
            else:
                # search more
                for n in G.neighbors(last_node):
                    if n.isupper():
                        # upper case, we just add
                        new_routes.append(r + [n])
                    else:
                        if n not in r:
                            new_routes.append(r + [n])

        routes = new_routes

    return len(completed_routes)

x = solve_with_loops('day_12_test_1.txt')
print(f"found {x} distinct routes (expect 10)")
x = solve_with_loops('day_12_test_2.txt')
print(f"found {x} distinct routes (expect 19)")
x = solve_with_loops('day_12_test_3.txt')
print(f"found {x} distinct routes (expect 226)")
x = solve_with_loops('day_12_input.txt')
print(f"found {x} distinct routes (expect 4573)")


def contains_no_doubles(r):
    '''
    >>> contains_no_doubles(['a', 'b', 'c'])
    True
    >>> contains_no_doubles(['a', 'b', 'c', 'b'])
    False
    '''
    c = Counter()
    for n in r:
        if n.islower() and n not in ('start', 'end'):
            c[n] += 1

    x = [v for v in c.values() if v > 1]
    return len(x) == 0



def solve_part_2_with_loops(filename):
    G = build_graph(filename)

    completed_routes = []
    routes = []
    routes.append(['start'])

    while len(routes) > 0:
        new_routes = []
        for r in routes:
            # new_routes = []
            last_node = r[-1]
            if last_node == 'end':
                # route is complete, add it to completed routes
                completed_routes.append(r)
                # print(f"completed {str(r)}")
            else:
                # search more
                for n in G.neighbors(last_node):
                    if n.isupper():
                        # upper case, we just add
                        new_routes.append(r + [n])
                    elif n in ('start', 'end'):
                        # start and end get visited exactly once
                        if (n not in r):
                            new_routes.append(r + [n])
                    else:
                        # lower case, we add if n is not in r
                        if (n not in r) or (n in r and contains_no_doubles(r)):
                            new_routes.append(r + [n])

        routes = new_routes

    # for r in completed_routes:
    #     print(r)

    return len(completed_routes)

x = solve_part_2_with_loops('day_12_test_1.txt')
print(f"found {x} distinct routes (expect 36)")
x = solve_part_2_with_loops('day_12_test_2.txt')
print(f"found {x} distinct routes (expect 103)")
x = solve_part_2_with_loops('day_12_test_3.txt')
print(f"found {x} distinct routes (expect 3509)")
x = solve_part_2_with_loops('day_12_input.txt')
print(f"found {x} distinct routes (expect 117509)")