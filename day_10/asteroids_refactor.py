from pathlib import Path
from collections import Counter, namedtuple
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


def relative_to_absolute(source, offset):
    """Return the actual coordinate location, reverse relative position"""
    return Point(source.x + offset.x, source.y + offset.y)


def calc_slope(source, destination):
    x, y = relative_position(source, destination)
    try:
        rise_run = Fraction(y, x)
        rise = rise_run.numerator
        run = rise_run.denominator
    except ZeroDivisionError:
        rise = 1
        run = 0
    if destination.y < source.y:
        rise = -abs(rise)
    else:
        rise = abs(rise)
    if destination.x < source.x:
        run = -abs(run)
    else:
        run = abs(run)
    return Slope(rise, run)


class AsteroidField:
    def __init__(self, file):
        self.field = read_points(file)
        self.min_x = min(point.x for point in self.field)
        self.max_x = max(point.x for point in self.field)
        self.min_y = min(point.y for point in self.field)
        self.max_y = max(point.y for point in self.field)
    
    def count_slopes(self, point):
        return len(set(calc_slope(point, dest) for dest in self.field if dest != point))
    
    def best(self):
        result = {point: self.count_slopes(point) for point in self.field}
        max_point = max(result, key=lambda k: result[k])
        return result[max_point], max_point


    def in_area(self, point):
        """Check if a point is within the asteroid field"""
        return (self.min_x <= point.x <= self.max_x) and (
            self.min_y <= point.y <= self.max_y
        )

    def max_sweep(self, point):
        """furthest distance from point to edge of field
        is the biggest fraction for sweepint possible
        """
        return max(
            point.x - self.min_x,
            self.max_x - point.max_x,
            point.y - self.min_y,
            self.max_y - point.y,
        )

    def circle_edges(self, point):
        # start directly above the point
        edge = Point(point.x, self.min_y)
        yield edge
        # move clockwise to the right
        while edge.x < self.max_x:
            edge = Point(edge.x + 1, edge.y)
            yield edge
        # down the right edge
        while edge.y < self.max_y:
            edge = Point(edge.x, edge.y + 1)
            yield edge
        # across the bottom
        while edge.x > self.min_x:
            edge = Point(edge.x - 1, edge.y)
            yield edge
        # back to the top
        while edge.y > self.min_y:
            edge = Point(edge.x, edge.y - 1)
            yield edge
        # back to the start
        while edge.x < point.x - 1:
            edge = Point(edge.x + 1, edge.y)
            yield edge



    def sweep(self, point):
        # maybe I can still do this as a generator?
        slopes = list()
        edges = [edge for edge in self.circle_edges(point)]
        for edge in edges:
            if point == edge:
                pass
            slope = calc_slope(point, edge)
            if slope not in slopes:
                slopes.append(slope)
        for slope in slopes:
            # print(f"EDGE: {edge}. SLOPE: {slope}")
            rise = slope.rise
            run = slope.run
            target = Point(point.x + run, point.y + rise)
            contact = False
            while self.in_area(target) and not contact:
                # print(f"EDGE: {edge}, TARGET: {target}")
                if target in self.field:
                    yield target
                    contact = True
                    # pass
                target = Point(target.x + run, target.y + rise)

    def observable_points(self):
        point_counter = Counter()
        for point in self.field:
            for _ in self.sweep(point):
                point_counter[point] += 1
        return point_counter

    def best_asteroid(self):
        counts = self.observable_points()
        max_point = max(counts, key=lambda k: counts[k])
        return counts[max_point], max_point


assert AsteroidField(here / "ex1.txt").best() == (8, Point(3, 4))
assert AsteroidField(here / "ex2.txt").best() == (33, Point(5, 8))
assert AsteroidField(here / "ex3.txt").best() == (35, Point(1, 2))
assert AsteroidField(here / "ex4.txt").best() == (41, Point(6, 3))
assert AsteroidField(here / "ex5.txt").best() == (210, Point(11, 13))
assert AsteroidField(here / "input.txt").best() == (256, Point(29, 28))

