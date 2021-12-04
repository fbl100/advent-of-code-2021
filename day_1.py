from functools import reduce

import more_itertools

def count_increasing(data):
    def is_increasing(a, b):
        return b > a
    windows = list(more_itertools.windowed(data, n=2, step=1))
    count = reduce(lambda count, i: count + is_increasing(i[0], i[1]), windows, 0)
    return count

with open("day_1_input.txt") as f:
    raw_data = [int(x.strip()) for x in f.readlines()]

print(count_increasing(raw_data))

# sliding window (3) sums
triples = list(more_itertools.windowed(raw_data, n=3, step=1))
sums = list(map(lambda x: sum(x), triples))
print(count_increasing(sums))


