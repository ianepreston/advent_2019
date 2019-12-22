from pathlib import Path
import sys
from itertools import permutations

libpath = Path(__file__).parent.parent
sys.path.append(str(libpath))
from adventop import IntCode

base = libpath.parent


def test_day2_1():
    inprog = [1, 0, 0, 0, 99]
    compy = IntCode(inprog)
    compy.run_to_completion()
    assert list(compy.work_prog) == [2, 0, 0, 0, 99]


def test_day2_2():
    inprog = [2, 3, 0, 3, 99]
    compy = IntCode(inprog)
    compy.run_to_completion()
    assert list(compy.work_prog) == [2, 3, 0, 6, 99]


def test_day2_3():
    inprog = base / "day_02" / "input.txt"
    compy = IntCode(inprog)
    compy.work_prog[1] = 12
    compy.work_prog[2] = 2
    compy.run_to_completion()
    assert compy.work_prog[0] == 2782414


def test_day2_4():
    inprog = base / "day_02" / "input.txt"

    def result_checker():
        for noun in range(100):
            for verb in range(100):
                compy = IntCode(inprog)
                compy.work_prog[1] = noun
                compy.work_prog[2] = verb
                compy.run_to_completion()
                if compy.work_prog[0] == 19690720:
                    return 100 * noun + verb

    assert result_checker() == 9820


def test_day5_1():
    inprog = base / "day_05" / "input.txt"
    compy = IntCode(inprog)
    compy.receive_input(1)
    results = compy.run_to_completion()
    assert results[-1] == 7839346


def test_day5_2():
    inprog = base / "day_05" / "input.txt"
    compy = IntCode(inprog)
    compy.receive_input(5)
    results = compy.run_to_completion()
    assert results[-1] == 447803


def run_amps(program, sequence):
    amp_in = 0
    for phase_setting in sequence:
        intcoder = IntCode(program).receive_input(phase_setting, amp_in)
        amp_in = intcoder.next_output()
    return amp_in


def max_thruster(program):
    return max((run_amps(program, sequence) for sequence in permutations(range(5))))


def test_day_7_1():
    here = base / "day_07"
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


def test_day_7_2():
    here = base / "day_07"
    assert cycle_amps((here / "ex4.txt"), (9, 8, 7, 6, 5)) == 139629729
    assert max_cycle_thruster(here / "ex4.txt") == 139629729
    assert max_cycle_thruster(here / "ex5.txt") == 18216
    assert max_cycle_thruster(here / "input.txt") == 35993240


def test_day_9_1():
    inputprog = base / "day_09/input.txt"
    boost_int = IntCode(inputprog)
    boost_int.receive_input(1)
    assert boost_int.run_to_completion()[0] == 2932210790


def test_day_9_2():
    EX = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    int_ex = IntCode(EX)
    assert list(int_ex.run_to_completion()) == EX


def test_day_9_3():
    EX = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    int_ex = IntCode(EX)
    assert int_ex.run_to_completion()[0] == 1219070632396864


def test_day_9_4():
    EX = [104, 1125899906842624, 99]
    int_ex = IntCode(EX)
    assert int_ex.run_to_completion()[0] == EX[1]


def test_day_9_5():
    EX = [109, -1, 4, 1, 99]
    int_ex = IntCode(EX)
    assert int_ex.run_to_completion()[0] == -1


def test_day_9_6():
    EX = [109, -1, 104, 1, 99]
    int_ex = IntCode(EX)
    assert int_ex.run_to_completion()[0] == 1


def test_day_9_7():
    EX = [109, -1, 204, 1, 99]
    int_ex = IntCode(EX)
    assert int_ex.run_to_completion()[0] == 109


def test_day_9_8():
    EX = [109, 1, 9, 2, 204, -6, 99]
    int_ex = IntCode(EX)
    assert int_ex.run_to_completion()[0] == 204


def test_day_9_9():
    EX = [109, 1, 109, 9, 204, -6, 99]
    int_ex = IntCode(EX)
    assert int_ex.run_to_completion()[0] == 204


def test_day_9_10():
    EX = [109, 1, 209, -1, 204, -106, 99]
    int_ex = IntCode(EX)
    assert int_ex.run_to_completion()[0] == 204


def test_day_9_10():
    EX = [109, 1, 3, 3, 204, 2, 99]
    int_ex = IntCode(EX)
    int_ex.receive_input(123)
    assert int_ex.run_to_completion()[0] == 123


def test_day_9_10():
    EX = [109, 1, 203, 2, 204, 2, 99]
    int_ex = IntCode(EX)
    int_ex.receive_input(123)
    assert int_ex.run_to_completion()[0] == 123
