from pathlib import Path
import sys
here = Path(__file__).parent
base = here.parent / "adventlib"
sys.path.append(str(base))

from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

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

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
    
    @property
    def slope(self):
        pass