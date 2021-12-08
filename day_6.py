import re
from collections import Counter


def parse_line(line):
    """
    >>> parse_line("3,4,3,1,2")
    {3: 2, 4: 1, 1: 1, 2: 1}
    """
    ret_val = Counter()

    for x in line.split(','):
        ret_val[int(x)] += 1

    return dict(ret_val)


def evolve(population: dict):
    """
    >>> evolve(parse_line("2,3,2,0,1"))
    {1: 2, 2: 1, 0: 1, 8: 1, 6: 1}
    """

    num_reset = 0
    new_vals = 0
    ret_val = dict()
    for (k, v) in population.items():
        next = k - 1
        if next < 0:
            new_vals += v
            num_reset = v
        else:
            ret_val[next] = v

    if new_vals > 0:
        ret_val[8] = new_vals
        if 6 not in ret_val:
            ret_val[6] = 0
        ret_val[6] += num_reset

    return ret_val

def process_file(file, days):
    with open(file) as f:
        population = parse_line(f.readline())
    # print(f'Initial state: {population}')

    for i in range(1, days+1):
        population = evolve(population)
        # print(f'After {i} days: {population}')

    return sum(population.values())


print(process_file("day_6_test.txt", 18))
print(process_file("day_6_test.txt", 80))
print(process_file("day_6_test.txt", 256))

print(process_file("day_6_input.txt", 18))
print(process_file("day_6_input.txt", 80))
print(process_file("day_6_input.txt", 256))

