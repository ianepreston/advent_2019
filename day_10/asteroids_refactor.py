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
        rise = Fraction.numerator
        run = Fraction.denominator
    except ZeroDivisionError:
        rise = 1
        run = 0
    return Slope(rise, run)


class AsteroidField:
    def __init__(self, file):
        self.field = read_points(file)
        self.min_x = min(point.x for point in self.field)
        self.max_x = max(point.x for point in self.field)
        self.min_y = min(point.y for point in self.field)
        self.max_y = max(point.y for point in self.field)

    def in_field(self, point):
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
            self.max_y - point.y
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
        
        

field = AsteroidField( here / "ex1.txt")
# print(field.field)
point = Point(3, 4)
for edge in field.circle_edges(point):
    print(edge)


