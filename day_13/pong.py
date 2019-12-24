from pathlib import Path
import sys
from collections import defaultdict, namedtuple

here = Path(__file__).parent.resolve()
base = here.parent / "adventlib"
sys.path.append(str(base))
from adventop import IntCode

Point = namedtuple("Point", ["x", "y"])
EMPTY = 0
WALL = 1
BLOCK = 2
HPAD = 3
BALL = 4


class Pong:
    def __init__(self, freeplay=False):
        self.grid = defaultdict(int)
        self.compy = IntCode(here / "input.txt")
        self.score = 0
        if freeplay:
            self.compy.work_prog[0] = 2

    def part1(self):
        while self.compy.running:
            x = self.compy.next_output()
            y = self.compy.next_output()
            pixel = self.compy.next_output()
            if x is not None and y is not None and pixel is not None:
                coord = Point(x, -y)
                self.grid[coord] = pixel
        return len([pix for pix in self.grid.values() if pix == BLOCK])


pong = Pong()
print(pong.part1())
pong = Pong(freeplay=True)

