from pathlib import Path
from collections import Counter, namedtuple
from math import atan2, dist, pi
from fractions import Fraction

Point = namedtuple("Point", ["x", "y"])
Slope = namedtuple("Slope", ["rise", "run"])
here = Path(__file__).parent


def read_points(file):
    with open(file, "r") as f:
        x = 0
        y = 0
        points = set()
        for line in f.readlines():
            x = 0
            for char in line:
                if char == "#":
                    points.add(Point(x, y))
                x += 1
            y += 1
    return points


def relative_position(source, destination):
    """return a point showing the x, y of destination relative to source
    e.g. if source is at (2, 4) and destination is at (3, 5) this will
    return (1, 1)
    """
    return Point(destination.x - source.x, destination.y - source.y)


def calc_radians(source, destination):
    """Not quite radians, but close enough"""
    x, y = relative_position(source, destination)
    rad = atan2(y, x)
    if y > 0 and x < 0:
        rad = (2 * pi) - rad
    return rad


class AsteroidField:
    def __init__(self, file):
        self.field = read_points(file)
        self.min_x = min(point.x for point in self.field)
        self.max_x = max(point.x for point in self.field)
        self.min_y = min(point.y for point in self.field)
        self.max_y = max(point.y for point in self.field)

    def count_slopes(self, point):
        return len(
            set(calc_radians(point, dest) for dest in self.field if dest != point)
        )

    def best(self):
        result = {point: self.count_slopes(point) for point in self.field}
        max_point = max(result, key=lambda k: result[k])
        return result[max_point], max_point


assert AsteroidField(here / "ex1.txt").best() == (8, Point(3, 4))
assert AsteroidField(here / "ex2.txt").best() == (33, Point(5, 8))
assert AsteroidField(here / "ex3.txt").best() == (35, Point(1, 2))
assert AsteroidField(here / "ex4.txt").best() == (41, Point(6, 3))
assert AsteroidField(here / "ex5.txt").best() == (210, Point(11, 13))
assert AsteroidField(here / "input.txt").best() == (256, Point(29, 28))

