from pathlib import Path
import re
from collections import namedtuple, Counter

here = Path(__file__).parent.resolve()

EX1 = here / "ex1.txt"
EX2 = here / "ex2.txt"
EX3 = here / "ex3.txt"
EX4 = here / "ex4.txt"
EX5 = here / "ex5.txt"
IN = here / "input.txt"

ALL_IN = [EX1, EX2, EX3, EX4, EX5, IN]

Precursor = namedtuple("Precursor", ["compound", "number"])


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
        self.precursors = list()

    def __repr__(self):
        return self.name

    def reaction(self):
        print("refactoring this")
        return None
        ore_count = 0
        compound_count = Counter()
        compound_queue = [self]
        while compound_queue:
            current_compound = compound_queue[-1]
            requirements = {
                precursor.compound: precursor.number
                for precursor in current_compound.precursors
            }
            if len(requirements) == 1 and list(requirements.keys())[0].name == "ORE":
                ore_count += list(requirements.values())[0]
                compound_count[current_compound] = current_compound.outnum
                compound_queue.pop()
            else:
                missing_reqs = [
                    precursor.compound
                    for precursor in current_compound.precursors
                    if precursor.number > compound_count[precursor.compound]
                ]
                if missing_reqs:
                    compound_queue.extend(missing_reqs)
                else:
                    for precursor in current_compound.precursors:
                        compound_count[precursor.compound] -= precursor.number
                    compound_queue.pop()
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


# def part1(file):
#     compounds = parse_compounds(file)
#     fuel = compounds["FUEL"]
#     return fuel.reaction()


# assert part1(EX1) == 31
# assert part1(EX2) == 165
# assert part1(EX3) == 13312
# assert part1(EX4) == 180697
# assert part1(EX5) == 2210736
# print(part1(IN))
