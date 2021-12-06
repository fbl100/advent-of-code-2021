import re


def parse_line(line):
    """
    >>> parse_line("8,0 -> 0,8")
    [[8, 0], [0, 8]]
    """
    m = re.search(r"(\d+),(\d+).*?(\d+),(\d+)", line)
    return [[int(m[1]), int(m[2])], [int(m[3]), int(m[4])]]


class Line(object):

    def __init__(self, line):
        """
        >>> L = Line("8,0 -> 0,8")
        >>> str(L)
        '8,0 -> 0,8'
        """
        [[x1, y1], [x2, y2]] = parse_line(line)
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def __str__(self):
        return f'{self._x1},{self._y1} -> {self._x2},{self._y2}'

    def is_horizontal(self):
        """
        >>> Line("8,0 -> 8,8").is_horizontal()
        False
        >>> Line("0,0 -> 8,0").is_horizontal()
        True
        """
        return self._y1 == self._y2

    def is_vertical(self):
        """
        >>> Line("8,0 -> 8,8").is_vertical()
        True
        >>> Line("0,0 -> 8,0").is_vertical()
        False
        """
        return self._x1 == self._x2

    def points(self):
        """
        >>> list(Line("0,0 -> 8,0").points())
        [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)]
        >>> list(Line("8,0 -> 8,8").points())
        [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8)]
        """
        if self.is_horizontal():
            x1 = min(self._x1, self._x2)
            x2 = max(self._x1, self._x2)
            for x in range(x1, x2 + 1):
                yield (x, self._y1)
        elif self.is_vertical():
            y1 = min(self._y1, self._y2)
            y2 = max(self._y1, self._y2)
            for y in range(y1, y2 + 1):
                yield (self._x1, y)
        else:
            # diagonal
            x1 = self._x1
            y1 = self._y1
            x2 = self._x2
            y2 = self._y2
            #
            # if self._x2 < self._x1:
            #     x1 = self._x2
            #     y1 = self._y2
            #     x2 = self._x1
            #     y2 = self._y1

            dx = 1
            dy = 1
            if x2 < x1:
                dx = -1
            if y2 < y1:
                dy = -1
            x = list(range(x1,x2+dx,dx))
            y = list(range(y1,y2+dy,dy))

            for p in zip(x,y):
                yield p


def process_file(file, func):
    with open(file) as f:
        lines = f.readlines()

    lines = [Line(x) for x in lines]
    lines = list(filter(lambda x: func(x), lines))

    d = dict()
    for l in lines:
        for p in l.points():
            if p in d:
                d[p] = d[p] + 1
            else:
                d[p] = 1

    points = {k: v for k, v in d.items() if v > 1}
    return len(points)


x = process_file("day_5_test.txt", lambda x: x.is_horizontal() or x.is_vertical())
print(f"count = {x}")
x = process_file("day_5_test.txt", lambda x: True)
print(f"count = {x}")

x = process_file("day_5_input.txt", lambda x: x.is_horizontal() or x.is_vertical())
print(f"count = {x}")
x = process_file("day_5_input.txt", lambda x: True)
print(f"count = {x}")