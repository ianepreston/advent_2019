from pathlib import Path
import re
import math
from collections import Counter

here = Path(__file__).parent.resolve()

EX1 = here / "ex1.txt"
EX2 = here / "ex2.txt"
EX3 = here / "ex3.txt"
EX4 = here / "ex4.txt"
EX5 = here / "ex5.txt"
IN = here / "input.txt"

ALL_IN = [EX1, EX2, EX3, EX4, EX5, IN]


def parse_line(input_str):
    rgx = r"(\d+) ([A-Z]+)"
    inputs, outputs = input_str.split(" => ")
    outnum, outcomp = re.match(rgx, outputs).groups()
    output = (outcomp, int(outnum))
    fin_in = dict()
    for entry in inputs.split(", "):
        num, comp = re.match(rgx, entry).groups()
        fin_in[comp] = int(num)
    return fin_in, output


class Compound:
    def __init__(self, name, outnum=None):
        self.name = name
        self.outnum = outnum
        # list of tuples format (compound, number required)
        self.precursors = list()
        self._depth = None

    def __repr__(self):
        return self.name

    def reaction(self, total_out=1):
        ore_count = 0
        compound_count = Counter()
        compound_count[self] += total_out
        while any(val > 0 for val in compound_count.values()):
            compound = next(
                iter(
                    compound
                    for compound, numreq in compound_count.items()
                    if numreq > 0
                )
            )
            numreq = compound_count[compound]
            reactions = math.ceil(numreq / compound.outnum)
            compound_count[compound] -= compound.outnum * reactions
            precursors = compound.precursors
            if len(precursors) == 1 and precursors[0][0].name == "ORE":
                ore, orenum = precursors[0]
                ore_count += orenum * reactions
            else:
                for compound, required in precursors:
                    compound_count[compound] += required * reactions
        return ore_count


def parse_compounds(in_file):
    compounds = dict()
    with open(in_file, "r") as f:
        for line in f.readlines():
            inputs, output = parse_line(line)
            if output[0] in compounds.keys():
                compounds[output[0]].outnum = output[1]
            else:
                compounds[output[0]] = Compound(*output)
            for precursor, number in inputs.items():
                if precursor not in compounds.keys():
                    compounds[precursor] = Compound(precursor)
                compounds[output[0]].precursors.append((compounds[precursor], number))
    return compounds


def check_outputs(in_file):
    """See if there's only one way to make each compound"""
    outputs = list()
    with open(in_file, "r") as f:
        for line in f.readlines():
            _, output = parse_line(line)
        outputs.append(output[0])
    assert len(outputs) == len(set(outputs))


for file in ALL_IN:
    check_outputs(file)


def validate_compounds(in_file):
    compounds = parse_compounds(in_file)
    for compound in compounds.values():
        if compound.name != "ORE":
            assert compound.outnum is not None
            for precursor in compound.precursors:
                precomp, prenum = precursor
                assert prenum is not None
                if precomp.name == "ORE":
                    assert len(precomp.precursors) == 0
                else:
                    assert precomp.outnum is not None


for file in ALL_IN:
    validate_compounds(file)


def part1(file):
    compounds = parse_compounds(file)
    fuel = compounds["FUEL"]
    return fuel.reaction()


def part2(file):
    so_much_ore = 1_000_000_000_000
    compounds = parse_compounds(file)
    fuel = compounds["FUEL"]
    # even if there's no savings I have to be able to make this much
    min_fuel = so_much_ore // fuel.reaction(total_out=1)
    # I don't know, this seems big enough
    max_fuel = min_fuel * 5
    mid_fuel = min_fuel + ((max_fuel - min_fuel) // 2)
    while mid_fuel != max_fuel and mid_fuel != min_fuel:
        if fuel.reaction(total_out=mid_fuel) > so_much_ore:
            max_fuel = mid_fuel
        else:
            min_fuel = mid_fuel
        mid_fuel = min_fuel + ((max_fuel - min_fuel) // 2)
    assert fuel.reaction(total_out=mid_fuel) <= so_much_ore
    if fuel.reaction(total_out=max_fuel) <= so_much_ore:
        return max_fuel
    else:
        return mid_fuel


assert part1(EX1) == 31
assert part1(EX2) == 165
assert part1(EX3) == 13_312
assert part1(EX4) == 180_697
assert part1(EX5) == 2_210_736
assert part1(IN) == 2_556_890

assert part2(EX3) == 82892753
assert part2(EX4) == 5586022
assert part2(EX5) == 460664
print(part2(IN))
