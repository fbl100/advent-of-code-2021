from bitarray import bitarray
from bitarray.util import ba2int


def most_common(bits, i):
    ones = sum([b[i] for b in bits])

    if ones >= len(bits) / 2:
        return 1
    else:
        return 0


def least_common(bits, i):
    if most_common(bits, i) == 1:
        return 0
    else:
        return 1


def day3(fileName):
    with open(fileName) as f:
        bits = [bitarray(x) for x in f.readlines()]

    num_bits = len(bits[0])
    gamma_bits = bitarray()
    for i in range(0, num_bits):
        x = most_common(bits, i)
        gamma_bits.append(x)

    gamma = ba2int(gamma_bits)
    epsilon = ba2int(~gamma_bits)

    return gamma, epsilon


def calc(bits, f):
    values = bits.copy()
    num_bits = len(values[0])
    for i in range(0, num_bits):
        if (len(values) > 1):
            c = f(values, i)
            values = list(filter(lambda x: x[i] == c, values))
    return ba2int(values[0])


def calc_o2(bits):
    return calc(bits, most_common)


def calc_c02(bits):
    return calc(bits, least_common)


def day3_2(fileName):
    with open(fileName) as f:
        bits = [bitarray(x) for x in f.readlines()]

    o2 = calc_o2(bits)
    co2 = calc_c02(bits)

    return o2, co2


gamma, epsilon = day3("day_3_input.txt")

print(f"gamma   = {gamma}")
print(f"epsilon = {epsilon}")
print(f"prod    = {gamma * epsilon}")

o2, co2 = day3_2("day_3_input.txt")

print(f"o2   = {o2}")
print(f"co2 = {co2}")
print(f"prod    = {o2 * co2}")
