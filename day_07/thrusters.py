from pathlib import Path
import sys

here = Path(__file__).parent
base = here.parent / "adventlib"
sys.path.append(str(base))
from adventop import opcoder, read_program

from itertools import permutations

# permutations(range(5))
def run_amps(program, sequence):
    amp_in = 0
    for phase_setting in sequence:
        amp_in = opcoder(program, [phase_setting, amp_in])[0]
    return amp_in


def max_thruster(program):
    return max((run_amps(program, sequence) for sequence in permutations(range(5))))


assert run_amps(read_program(here / "ex1.txt"), (4, 3, 2, 1, 0)) == 43210
assert max_thruster(read_program(here / "ex1.txt")) == 43210
assert max_thruster(read_program(here / "ex2.txt")) == 54321
assert max_thruster(read_program(here / "ex3.txt")) == 65210
print(max_thruster(read_program(here / "input.txt")))
