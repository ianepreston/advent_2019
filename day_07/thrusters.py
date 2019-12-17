import sys
from itertools import permutations
from pathlib import Path

here = Path(__file__).parent.resolve()
base = here.parent / "adventlib"
sys.path.append(str(base))
from adventop import IntCode


def run_amps(program, sequence):
    amp_in = 0
    for phase_setting in sequence:
        intcoder = IntCode(program).receive_input(phase_setting, amp_in)
        amp_in = intcoder.next_output()
    return amp_in


def max_thruster(program):
    return max((run_amps(program, sequence) for sequence in permutations(range(5))))


assert run_amps((here / "ex1.txt"), (4, 3, 2, 1, 0)) == 43210
assert max_thruster(here / "ex1.txt") == 43210
assert max_thruster(here / "ex2.txt") == 54321
assert max_thruster(here / "ex3.txt") == 65210
assert max_thruster(here / "input.txt") == 368584


def cycle_amps(program, sequence):
    amp_in = 0
    int_coders = [IntCode(program).receive_input(seq) for seq in sequence]
    while any(coder.running for coder in int_coders):
        for coder in int_coders:
            coder.receive_input(amp_in)
            amp_in = coder.next_output()
    return int_coders[-1].outputs[-1]


def max_cycle_thruster(program):
    return max(
        (cycle_amps(program, sequence) for sequence in permutations(range(5, 10)))
    )


assert cycle_amps((here / "ex4.txt"), (9, 8, 7, 6, 5)) == 139629729
assert max_cycle_thruster(here / "ex4.txt") == 139629729
assert max_cycle_thruster(here / "ex5.txt") == 18216
print(max_cycle_thruster(here / "input.txt"))
