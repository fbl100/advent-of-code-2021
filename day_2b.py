def split_line(line):
    tokens = line.split()
    return tokens[0], tokens[1]



with open("day_2_input.txt") as f:
    lines = f.readlines()

commands = list(map(lambda line: split_line(line), lines))

h = 0
d = 0
aim = 0

def do_forward(x):
    global h, d, aim
    h += x
    d += (aim * x)

def do_up(x):
    global aim
    aim -= x

def do_down(x):
    global aim
    aim += x


dispatch = {
    'forward' : do_forward,
    'down': do_down,
    'up': do_up,
}

for c in commands:
    dispatch[c[0]](int(c[1]))

print(d)
print(h)
print(d*h)