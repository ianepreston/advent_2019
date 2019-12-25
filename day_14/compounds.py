from pathlib import Path
import re
from collections import namedtuple, defaultdict
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
    output = Precursor(outcomp, int(outnum))
    fin_in = list()
    for entry in inputs.split(", "):
        num, comp = re.match(rgx, entry).groups()
        fin_in.append(Precursor(comp, int(num)))
    return fin_in, output

class Compound:
    def __init__(self, name, outnum=None):
        self.name = name
        self.outnum = outnum
        self.precursors = list()
    
    def reaction(self):
        pass

def check_outputs(in_file):
    """See if there's only one way to make each compound"""
    outputs = list()
    with open(in_file, "r") as f:
        for line in f.readlines():
            _, output = parse_line(line)
        outputs.append(output.compound)
    assert len(outputs) == len(set(outputs))

for file in ALL_IN:
    check_outputs(file)

def parse_compounds(in_file):
    compounds = dict()
    with open(in_file, "r") as f:
        for line in f.readlines():
            inputs, output = parse_line(line)
            if output.compound in compounds.keys():
                compounds[output.compound].outnum = output.number
            else:
                compounds[output.compound] = Compound(output.compound, output.number)
            for comp_in in inputs:
                if comp_in.compound not in compounds.keys():
                    compounds[comp_in.compound] = Compound(comp_in.compound)
                compounds[output.compound].precursors.append(Precursor(compounds[comp_in.compound], comp_in.number))
    return compounds

def validate_compounds(in_file):
    compounds = parse_compounds(in_file)
    for compound in compounds.values():
        if compound.name != "ORE":
            assert compound.outnum is not None
            for precursor in compound.precursors:
                if precursor.compound.name == "ORE":
                    assert len(precursor.compound.precursors) == 0
                else:
                    assert precursor.compound.outnum is not None

for file in ALL_IN:
    validate_compounds(file)



