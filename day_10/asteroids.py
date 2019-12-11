from pathlib import Path
import sys

here = Path(__file__).parent
base = here.parent / "adventlib"
sys.path.append(str(base))

from collections import namedtuple, Counter

Point = namedtuple("Point", ["x", "y"])
LineEQ = namedtuple("LineEQ", ["m", "b"])


def read_points(file):
    with open(file, "r") as f:
        x = 0
        y = 0
        points = []
        for line in f.readlines():
            x = 0
            for char in line:
                if char == "#":
                    points.append(Point(x, y))
                x += 1
            y += 1
    return points


def calc_slope(point1, point2):
    if point1.x == point2.x:
        return None
    else:
        m = (point1.y - point2.y) / (point1.x - point2.x)
        b = -(m * point1.x - point1.y)
        return LineEQ(m, b)


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    @property
    def min_x(self):
        return min(self.point1.x, self.point2.x)

    @property
    def max_x(self):
        return max(self.point1.x, self.point2.x)

    @property
    def min_y(self):
        return min(self.point1.y, self.point2.y)

    @property
    def max_y(self):
        return max(self.point1.y, self.point2.y)

    def point_in_box(self, point):
        in_x = self.min_x <= point.x <= self.max_x
        in_y = self.min_y <= point.y <= self.max_y
        return in_x & in_y

    def point_on_line(self, point):
        if not self.point_in_box(point):
            return False
        elif self.point1.x == self.point2.x:
            return self.min_y < point.y < self.max_y
        elif self.point1.y == self.point2.y:
            return self.min_x < point.x < self.max_x
        else:
            return calc_slope(self.point1, self.point2) == calc_slope(
                self.point1, point
            )

test = Line(Point(3, 4), Point(1, 0))
assert test.point_on_line(Point(2, 2))
tp = Point(3, 4)
test = Line(tp, tp)
assert not test.point_on_line(Point(2,2))
assert not test.point_on_line(tp)

def observable_points(points):
    point_counter = Counter()
    for source in points:
        for dest in points:
            line = Line(source, dest)
            if all(not line.point_on_line(point) for point in points if point != source):
                point_counter[source] += 1
    return point_counter

def best_asteroid(points):
    point_counter = observable_points(points)
    max_key = max(point_counter, key=lambda k: point_counter[k])
    return point_counter[max_key], max_key

print(best_asteroid(read_points(here / "ex1.txt")))
# Nope, getting 4 with 1,2 instead of 8 with 3,4
