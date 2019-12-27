from pathlib import Path
import re
import math
from collections import OrderedDict, Counter

here = Path(__file__).parent.resolve()

EX1 = here / "ex1.txt"
EX2 = here / "ex2.txt"
EX3 = here / "ex3.txt"
EX4 = here / "ex4.txt"
EX5 = here / "ex5.txt"
IN = here / "input.txt"

ALL_IN = [EX1, EX2, EX3, EX4, EX5, IN]


def ceildiv(a, b):
    return -(-a // b)


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
    
    def calc_depth(self):
        precursors = self.precursors
        if len(precursors) == 1 and precursors[0][0].name == "ORE":
            return 1
        elif self.name == "ORE":
            return 0
        else:
            return 1 + max(precursor[0].depth for precursor in precursors)
    
    @property
    def depth(self):
        if self._depth is None:
            self._depth = self.calc_depth()
        return self._depth
    
    def reaction(self):
        ore_count = 0
        compound_count = Counter()
        compound_count[self] += 1
        while any(val >0 for val in compound_count.values()):
            compound = next(iter(compound for compound, numreq in compound_count.items() if numreq > 0))
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
            



    def reaction_old(self):
        ore_count = 0
        compound_count = Counter()
        compound_queue = OrderedDict()
        compound_queue[self] = 1
        while compound_queue:
            compound_queue = OrderedDict(sorted(compound_queue.items(), key=lambda x: x[0].depth, reverse=True))
            compound, numreq = compound_queue.popitem(last=False)
            if numreq <= compound_count[compound]:
                compound_count[compound] -= numreq
            else:
                precursors = compound.precursors
                if len(precursors) == 1 and precursors[0][0].name == "ORE":
                    ore, orenum = precursors[0]
                    compout = compound.outnum
                    reactions = ceildiv(numreq, compout)
                    ore_count += orenum * reactions
                    compound_count[compound] += (reactions * compout) -numreq
                else:
                    for compound, required in precursors:
                        tomake = ceildiv(required * numreq, compound.outnum)
                        if compound in compound_queue.keys():
                            compound_queue[compound] += tomake 
                        else:
                            compound_queue[compound] = tomake 
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


assert part1(EX1) == 31
assert part1(EX2) == 165
assert part1(EX3) == 13312
assert part1(EX4) == 180697
assert part1(EX5) == 2210736
print(part1(IN))
# compounds = parse_compounds(EX1)
# compounds = OrderedDict(compounds)
# ore = compounds["ORE"]