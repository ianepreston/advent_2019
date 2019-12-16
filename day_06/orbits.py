import re
from pathlib import Path

here = Path(__file__).parent
base = here.parent / "adventlib"
EX = here / "example.txt"
IN = here / "input.txt"


def parse_orbit(orbit_str):
    rgx = r"(\w+)\)(\w+)"
    orbits, mass = re.match(rgx, orbit_str).groups()
    return orbits, mass


assert parse_orbit("HGT)HZ8") == ("HGT", "HZ8")


def read_input(file):
    with open(file, "r") as f:
        return (parse_orbit(line) for line in f.readlines())


class SpaceObject:
    def __init__(self, name, orbits):
        self.name = name
        self.orbits = orbits
        self.orbited_by = list()

    def parent_orbit_count(self):
        if self.orbits is None:
            return 0
        else:
            return 1 + self.orbits.parent_orbit_count()

    def child_orbit_count(self):
        orbit_count = 0
        orbit_queue = [self]
        while orbit_queue:
            mass = orbit_queue.pop(0)
            orbit_count += mass.parent_orbit_count()
            orbit_queue.extend(mass.orbited_by)
        return orbit_count


def build_solar_system(file):
    solar_dict = dict()
    for orbits, mass in read_input(file):
        if orbits not in solar_dict:
            solar_dict[orbits] = SpaceObject(orbits, None)
        if mass not in solar_dict:
            solar_dict[mass] = SpaceObject(mass, solar_dict[orbits])
        else:
            solar_dict[mass].orbits = solar_dict[orbits]
        solar_dict[orbits].orbited_by.append(solar_dict[mass])
    return solar_dict["COM"], solar_dict


def part1(file):
    com, _ = build_solar_system(file)
    return com.child_orbit_count()


assert part1(EX) == 42
print(part1(IN))
