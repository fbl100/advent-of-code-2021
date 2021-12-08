import numpy as np

def score(positions : list[int], a):
    return sum([abs(x - a) for x in positions])

def score_2(positions: list[int], a):

    def score_x(x):
        dx = abs(x - a)
        sum = dx * (dx+1) / 2
        return sum

    return sum(score_x(x) for x in positions)


def process_file(file_name, func, debug = False):
    with open(file_name) as f:
        values = [int(x) for x in f.readline().split(",")]

    min = np.min(values)
    max = np.max(values)

    best = -1
    best_score = 100000000000

    for i in range(min, max+1):
        xx = func(values, i)

        if debug:
            print(f"{i}: {xx}")

        if xx < best_score:
            best_score = xx
            best = i

    print(f"Depth = {best}, Score = {best_score}")

process_file("day_7_test.txt", score, False)
process_file("day_7_test.txt", score_2, False)
process_file("day_7_input.txt", score, False)
process_file("day_7_input.txt", score_2, False)