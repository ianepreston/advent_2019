from pathlib import Path
import sys
from collections import namedtuple

here = Path(__file__).parent.resolve()
base = here.parent / "adventlib"
sys.path.append(str(base))
from adventop import IntCode

WALL = 0
STEP = 1
OXYGEN = 2

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

COMPASS = [NORTH, SOUTH, EAST, WEST]

Coord = namedtuple("Coord", ["x", "y"])


class Route:
    def __init__(self, coord, precedent=None):
        self.coord = coord
        self.precedent = precedent
        self.antecdent = None
        if self.precedent is not None:
            self.precedent.antecdent = self

    def distance(self):
        if self.precedent is None:
            return 0
        else:
            return 1 + self.precedent.distance()

    def step(self):
        if self.precedent is None:
            return None
        x, y = self.coord
        oldx, oldy = self.precedent.coord
        delta_x = x - oldx
        delta_y = y - oldy
        # I screwed something up if this isn't right
        assert delta_x == 0 or delta_y == 0
        if delta_x == 1:
            return EAST
        elif delta_x == -1:
            return WEST
        elif delta_y == 1:
            return NORTH
        elif delta_y == -1:
            return SOUTH
        else:
            raise ValueError(f"Something wrong with my deltas x {delta_x}, y {delta_y}")

    def backwards(self):
        last_step = self.step()
        if last_step is None:
            return None
        elif last_step == NORTH:
            return SOUTH
        elif last_step == SOUTH:
            return NORTH
        elif last_step == WEST:
            return EAST
        elif last_step == EAST:
            return WEST
        else:
            raise ValueError("I guess step() is broken?")

    def steps(self):
        curr_route = self
        step_list = list()
        while curr_route.step() is not None:
            step_list.append(curr_route.step())
            curr_route = curr_route.precedent
        step_list.reverse()
        return step_list


# going to need to do breadth first search somehow
class RepairBot:
    def __init__(self):
        self.reset()

    def reset(self):
        self.compy = IntCode(here / "input.txt")
        self.route = Route(Coord(0, 0))
        self.found_oxygen = False

    def trystep(self, direction):
        self.compy.receive_input(direction)
        result = self.compy.next_output()
        if result == WALL:
            return False
        elif result == STEP:
            return True
        elif result == OXYGEN:
            self.found_oxygen = True
            return True
        else:
            raise ValueError(f"Step attempt returned invalid result: {result}")

    def update_route(self, direction):
        base_coord = self.route.coord
        if direction == NORTH:
            new_coord = Coord(base_coord.x, base_coord.y + 1)
        elif direction == SOUTH:
            new_coord = Coord(base_coord.x, base_coord.y - 1)
        elif direction == WEST:
            new_coord = Coord(base_coord.x - 1, base_coord.y)
        elif direction == EAST:
            new_coord = Coord(base_coord.x + 1, base_coord.y)
        else:
            raise ValueError(f"Invalid direction {direction}")
        self.route = Route(new_coord, self.route)

    def find_oxygen(self):
        route_queue = [self.route]
        while True:
            curr_route = route_queue.pop(0)
            back_step = curr_route.backwards()
            possible_steps = [step for step in COMPASS if step != back_step]
            for next_step in possible_steps:
                get_here = curr_route.steps()
                self.reset()
                for step in get_here:
                    assert self.trystep(step)
                    self.update_route(step)
                if self.trystep(next_step):
                    self.update_route(next_step)
                    if self.found_oxygen:
                        return self.route.distance(), self.route.steps()
                    route_queue.append(self.route)

    def oxygen_fill(self):
        self.reset()
        _, oxygen_path = self.find_oxygen()

        def start_at_oxygen():
            self.reset()
            for step in oxygen_path:
                assert self.trystep(step)

        # Now oxygen is the 0 point
        start_at_oxygen()
        route_queue = [self.route]
        while route_queue:
            curr_route = route_queue.pop(0)
            back_step = curr_route.backwards()
            possible_steps = [step for step in COMPASS if step != back_step]
            for next_step in possible_steps:
                get_here = curr_route.steps()
                start_at_oxygen()
                for step in get_here:
                    assert self.trystep(step)
                    self.update_route(step)
                if self.trystep(next_step):
                    self.update_route(next_step)
                    route_queue.append(self.route)
        return curr_route.distance()


bot = RepairBot()
print(bot.find_oxygen()[0])
bot = RepairBot()
print(bot.oxygen_fill())

