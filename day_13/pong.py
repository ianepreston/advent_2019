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

    def update_game(self):
        x = self.compy.next_output()
        y = self.compy.next_output()
        val = self.compy.next_output()
        if all(arg is not None for arg in (x, y, val)):
            if x == -1 and y == 0:
                self.score = val
            else:
                coord = Point(x, -y)
                self.grid[coord] = val

    def find_ball(self):
        ball_coords = [coord for coord, pix in self.grid.items() if pix == BALL]
        assert len(ball_coords) == 1
        return ball_coords[0]

    def find_paddle(self):
        paddle_coords = [coord for coord, pix in self.grid.items() if pix == HPAD]
        assert len(paddle_coords) == 1
        return paddle_coords[0]

    def move_jstick(self):
        ball_x = self.find_ball().x
        paddle_x = self.find_paddle().x
        if ball_x < paddle_x:
            self.compy.receive_input(-1)
        elif ball_x > paddle_x:
            self.compy.receive_input(1)
        else:
            self.compy.receive_input(0)

    @property
    def blocks_gone(self):
        num_blocks = len([pix for pix in self.grid.values() if pix == BLOCK])
        return num_blocks == 0 and len(self.grid) >= 684

    def win_game(self):
        while not self.blocks_gone:
            next_step = self.compy.run_to_next_io()
            if next_step == 3:
                self.move_jstick()
                self.compy.execute_op()
            elif next_step == 4:
                self.update_game()
        while self.compy.running:
            self.update_game()
        return self.score

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
assert pong.part1() == 251
pong = Pong(freeplay=True)
assert pong.win_game() == 12779
