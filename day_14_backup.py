import sys
import itertools
from collections import defaultdict, Counter, deque
import re


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

    current = template
    for i in range(0, num_steps):
        inserts = list()
        for k, v in substitutions.items():
            indices = [m.start()+1 for m in re.finditer(k, current)]
            for index in indices:
                inserts.append((index, v))

        inserts.sort(key=lambda c: c[0], reverse=True)

        for index,char in inserts:
            pre = current[:index]
            post = current[index:]
            current = pre + char + post

        c = Counter()
        for ch in current:
            c[ch] += 1

        mn = min(c.values())
        mx = max(c.values())
        print(f"[{i+1}]: {mx}-{mn}={mx-mn} len={len(current)}")
        print(c)
        print(current)


process_file("day_14_test.txt", 10)
# process_file("day_14_input.txt", 10)
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