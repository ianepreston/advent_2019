from pathlib import Path
from itertools import permutations
from collections import namedtuple
import re

here = Path(__file__).parent


EX1 = here / "ex1.txt"
EX2 = here / "ex2.txt"
INPUT = here / "input.txt"


class Moon:
    def __init__(self, start_pos):
        self.position = start_pos
        self.velocity = [0, 0, 0]

    def apply_gravity(self, other_moon):
        for dimension in range(3):
            if self.position[dimension] < other_moon.position[dimension]:
                self.velocity[dimension] += 1
            elif self.position[dimension] > other_moon.position[dimension]:
                self.velocity[dimension] -= 1

    def apply_velocity(self):
        for dimension in range(3):
            self.position[dimension] += self.velocity[dimension]

    @property
    def potential_energy(self):
        return sum(abs(pos) for pos in self.position)

    @property
    def kinetic_energy(self):
        return sum(abs(vel) for vel in self.velocity)

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy


def parse_coord(input_str):
    rgx = r"<x=(-?[0-9]\d*), y=(-?[0-9]\d*), z=(-?[0-9]\d*)>"
    match = re.match(rgx, input_str)
    coord = [int(num) for num in match.groups()]
    return coord


class System:
    def __init__(self, filename):
        with open(filename, "r") as f:
            self.moons = [Moon(parse_coord(line)) for line in f.readlines()]
        self.cycles = 0

    def simulate_step(self):
        for moon1, moon2 in permutations(self.moons, 2):
            moon1.apply_gravity(moon2)
        for moon in self.moons:
            moon.apply_velocity()
        self.cycles += 1

    @property
    def system_energy(self):
        return sum(moon.total_energy for moon in self.moons)


ex1_sys = System(EX1)
for _ in range(10):
    ex1_sys.simulate_step()

assert ex1_sys.system_energy == 179

ex2_sys = System(EX2)
for _ in range(100):
    ex2_sys.simulate_step()

assert ex2_sys.system_energy == 1940

sys = System(INPUT)
for _ in range(1_000):
    sys.simulate_step()

print(sys.system_energy)
