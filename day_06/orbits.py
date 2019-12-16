import re
from pathlib import Path

here = Path(__file__).parent
base = here.parent / "adventlib"
EX = here / "example.txt"
EX2 = here / "example2.txt"
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

    def path_to_com(self):
        path_list = list()
        mass = self.orbits
        while mass is not None:
            path_list.append(mass)
            mass = mass.orbits
        return path_list


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


def part2(file):
    com, solar_dict = build_solar_system(file)
    me = solar_dict["YOU"]
    santa = solar_dict["SAN"]
    santa_path = santa.path_to_com()
    me_path = me.path_to_com()
    if santa in me_path:
        return me_path.index(santa) - 1
    elif me in santa_path:
        return santa_path.index(me) - 1
    else:
        common_intersect = set(santa_path).intersection(set(me_path))
        greatest_common_intersect = [
            intersect
            for intersect in common_intersect
            if intersect.parent_orbit_count()
            == max(intersect.parent_orbit_count() for intersect in common_intersect)
        ]
        assert len(greatest_common_intersect) == 1
        common_intersect = greatest_common_intersect[0]
        me_steps = me_path.index(common_intersect)
        santa_steps = santa_path.index(common_intersect)
        return me_steps + santa_steps


assert part2(EX2) == 4
print(part2(IN))
