from pathlib import Path
from collections import namedtuple, defaultdict
import sys

here = Path(__file__).parent.resolve()
base = here.parent / "adventlib"
sys.path.append(str(base))
from adventop import IntCode

Point = namedtuple("Point", ["x", "y"])
BLACK = 0
WHITE = 1
TURNLEFT = 0
TURNRIGHT = 1
UP = Point(0, 1)
LEFT = Point(-1, 0)
DOWN = Point(0, -1)
RIGHT = Point(1, 0)


class Robot:
    def __init__(self, startwhite=False):
        self.compy = IntCode(here / "input.txt")
        self.hull = defaultdict(int)
        self.position = Point(0, 0)
        self.direction = UP
        self.painted_tiles = set()
        if startwhite:
            self.hull[self.position] = WHITE

    def turn(self, direction):
        turns = [UP, RIGHT, DOWN, LEFT]
        curr_index = turns.index(self.direction)
        if direction == TURNLEFT:
            new_index = curr_index - 1
        if direction == TURNRIGHT:
            new_index = curr_index + 1
            if new_index == len(turns):
                new_index = 0
        self.direction = turns[new_index]

    def step(self):
        self.position = Point(
            self.position.x + self.direction.x, self.position.y + self.direction.y
        )

    def run(self):
        while self.compy.running:
            next_input = self.hull[self.position]
            self.compy.receive_input(next_input)
            colour = self.compy.next_output()
            direction = self.compy.next_output()
            self.hull[self.position] = colour
            self.painted_tiles.add(self.position)
            if direction is not None:
                self.turn(direction)
                self.step()

    def part1(self):
        self.run()
        return len(self.painted_tiles)

    def paint_tiles(self):
        self.run()
        min_x = min(self.painted_tiles, key=lambda point: point.x).x
        max_x = max(self.painted_tiles, key=lambda point: point.x).x
        min_y = min(self.painted_tiles, key=lambda point: point.y).y
        max_y = max(self.painted_tiles, key=lambda point: point.y).y
        # Always with the y coordinates upside down messing with me
        for y in range(max_y, min_y - 1, -1):
            for x in range(min_x, max_x + 1):
                point = Point(x, y)
                if x == max_x:
                    end = "\n"
                else:
                    end = ""
                color = self.hull[point]
                if color == BLACK:
                    print(" ", end=end)
                else:
                    print("#", end=end)


robot = Robot()
print(robot.part1())
robot = Robot(startwhite=True)
robot.paint_tiles()

