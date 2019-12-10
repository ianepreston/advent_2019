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
        if ~self.point_in_box(point):
            return False
        if self.point1.x == self.point2.x:
            return self.min_y < point.y < self.max_y
        if self.point1.y == self.point2.y:
            return self.min_x < point.x < self.max_x
        

