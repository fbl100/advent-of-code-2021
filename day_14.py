import sys
import itertools
import more_itertools
from collections import defaultdict, Counter, deque
import re

from more_itertools import sliding_window


def pairs(s):
    '''
    >>> pairs("NCCB")
    ['NC', 'CC', 'CB']
    '''
    retval = ["".join(c) for c in sliding_window(s,2)]
    return retval


def process_file(filename, num_steps):
    regex = re.compile(r"(.*?) -> (.*)")

    with open(filename) as f:
        template = f.readline().strip()
        f.readline()
        substitutions = dict()
        for line in f.readlines():

            if line.strip() == "":
                continue
            m = regex.match(line)
            if m:
                key = m.group(1)
                val = m.group(2)
                substitutions[key] = val
    print(substitutions)

    letter_count = Counter(c for c in template)
    current_pairs = Counter(pairs(template))

    print(letter_count)
    print(current_pairs)

    for i in range(0, num_steps):
        new_pairs = Counter()
        for (pair,count) in current_pairs.items():
            sub = substitutions[pair]
            new_pairs[f"{pair[0]}{sub}"] += count
            new_pairs[f"{sub}{pair[1]}"] += count
            letter_count[sub] += count

        current_pairs = new_pairs
        mn = min(letter_count.values())
        mx = max(letter_count.values())
        s = sum(letter_count.values())
        print(f"[{i+1}]: {mx - mn} // {s}")



process_file("day_14_test.txt", 10)
process_file("day_14_input.txt", 10)
print("$$$")
process_file("day_14_test.txt", 40)
print("$$$")
process_file("day_14_input.txt", 400)
#
# NCNBCHB
# NCNBCHB
# NCNBCHB


# NBCCNBBBCBHCB
# NBCCNBBBCBHCB
# NBCCNBBBCBHCB

# NBBBCNCCNBNBBCHBHHBCB
# NBBBCNCCNBNBBCHBHHBCB
# NBBBCNCCNBBNBBBCHBHHBCHB
# NBBNBBBCCNBCNCNBBNBBCBHCBHHNHBCHB
# NBBNBBBCCNBCNCNBBNBBCBHCBHHNHBCHB
# NBBNBBBCCNBCNCNBBNBBCBHCBHHNHBCHB
