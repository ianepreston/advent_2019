from pathlib import Path
from collections import namedtuple, defaultdict
from math import atan2, dist, pi
from fractions import Fraction

Point = namedtuple("Point", ["x", "y"])
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
    return (1, -1)
    I reverse on the y axis because the stupid coordinate system is negative in that direction
    """
    return Point(destination.x - source.x, source.y - destination.y)


def calc_radians(source, destination):
    """Not quite radians, but close enough"""
    x, y = relative_position(source, destination)
    rad = atan2(y, x)
    if y >= 0 and x < 0:
        rad = -(2 * pi) + rad
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

    def rank_fields(self, point):
        angle_dict = defaultdict(list)
        for dest in self.field:
            rads = calc_radians(point, dest)
            angle_dict[rads].append(dest)
        for points in angle_dict.values():
            points.sort(key=lambda x: dist(point, x), reverse=True)
        while angle_dict:
            keys = angle_dict.keys()
            keys = sorted(keys, reverse=True)
            for key in keys:
                rad_points = angle_dict[key]
                yield rad_points.pop()
                if not rad_points:
                    del angle_dict[key]
        

    def best(self):
        result = {point: self.count_slopes(point) for point in self.field}
        max_point = max(result, key=lambda k: result[k])
        return result[max_point], max_point

    def part2(self):
        _, base = self.best()
        return [point for point in self.rank_fields(base)]


assert AsteroidField(here / "ex1.txt").best() == (8, Point(3, 4))
assert AsteroidField(here / "ex2.txt").best() == (33, Point(5, 8))
assert AsteroidField(here / "ex3.txt").best() == (35, Point(1, 2))
assert AsteroidField(here / "ex4.txt").best() == (41, Point(6, 3))
assert AsteroidField(here / "ex5.txt").best() == (210, Point(11, 13))
assert AsteroidField(here / "input.txt").best() == (256, Point(29, 28))

ex5_field = AsteroidField(here / "ex5.txt")
ex5_ranks = ex5_field.part2()
assert ex5_ranks[199] == Point(8,2)

fin_field = AsteroidField(here / "input.txt")
fin_point = fin_field.part2()[199]
answer = fin_point.x * 100 + fin_point.y
print(answer)