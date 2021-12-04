def split_line(line):
    tokens = line.split()
    return tokens[0], tokens[1]



with open("day_2_input.txt") as f:
    lines = f.readlines()

commands = list(map(lambda line: split_line(line), lines))

h = 0
d = 0

def do_forward(x):
    global h
    h += x

def do_up(y):
    global d
    d -= y

def do_down(y):
    global d
    d += y


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