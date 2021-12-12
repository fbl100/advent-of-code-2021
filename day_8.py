import re
from collections import Counter
from functools import reduce

digit2string = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg"
}

string2digit = { v:k for k,v in digit2string.items()}


def parse_line(line):
    """
    >>> parse_line("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
    {'digits': ['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'], 'values': ['cdfeb', 'fcadb', 'cdfeb', 'cdbaf']}
    """
    digits, values = line.split('|')

    ret_val = {
        "digits": re.split('\s+', digits.strip()),
        "values": re.split('\s+', values.strip())
    }

    return ret_val


def process_file(filename):
    with open(filename) as f:
        lines = [parse_line(x) for x in f.readlines()]

    values_only = reduce(list.__add__, [x['values'] for x in lines])
    filtered = [x for x in values_only if len(x) in (2, 3, 4, 7)]
    print(f"{len(filtered)} unique instances")

def create_decoder(digits):
    """
    >>>
    :param digits:
    :return:
    """
    counter = Counter()
    for d in digits:
        for c in d:
            counter[c] += 1

    counter = dict(counter)

    # first, pull the ones with length 2 and 3
    # the 'a' is the odd man out here
    # now, count the characters
    # the one that is not 'a' that has 8 instances is 'c'
    # the one that is not 'c' from the 1 is going to be 'f'

    # a b c d e f g
    # x   x     x

    # b has 6 instance
    # e has 4 instances
    # d and g are remaining, each with 7

    # the 4 has 4 items
    # remove b,c and f and you're left with d
    # g ramains


    decoder = {}

    # step 1: determine 'a'
    one = next(x for x in digits if len(x) == 2)
    seven = next(x for x in digits if len(x) == 3)
    four = next(x for x in digits if len(x) == 4)
    # print(f"one   : {one}")
    # print(f"seven : {seven}")

    (a,) = set(seven) - set(one)
    decoder[a] = 'a'

    # remove a from the counter list
    del counter[a]
    # print(counter)

    # get the remaining one with 8 instance
    c = next(k for (k, v) in counter.items() if v == 8)
    decoder[c] = 'c'

    (f,) = set(one) - set(c)
    decoder[f] = 'f'

    del counter[c]
    del counter[f]

    b = next(k for (k, v) in counter.items() if v == 6)
    del counter[b]
    e = next(k for (k, v) in counter.items() if v == 4)
    del counter[e]

    decoder[b] = 'b'
    decoder[e] = 'e'

    (d,) = set(four) - {b,c,f}
    decoder[d] = 'd'
    del counter[d]

    g = next(iter(counter.keys()))
    decoder[g] = 'g'


    return decoder

def decode_value(digit, decoder):

    s = ''
    for c in digit:
        s += decoder[c]

    s = "".join(sorted(s))
    return string2digit[s]

def decode_line(line):
    digits = line['digits']

    decoder = create_decoder(digits)

    num = ''
    for v in line['values']:
        x = decode_value(v, decoder)
        num += str(x)

    return int(num)







def decode(filename):
    with open(filename) as f:
        lines = [parse_line(x) for x in f.readlines()]

    nums = [decode_line(l) for l in lines]

    print(f"sum: {sum(nums)}")


c = Counter()
for k, v in sorted(digit2string.items(), key=lambda x: len(x[1])):
    print(f"{k} -> {len(v)}")
    for ch in v:
        c[ch] += 1

print(c)

process_file("day_8_test.txt")
process_file("day_8_input.txt")

decode("day_8_test.txt")
decode("day_8_input.txt")
