from pathlib import Path
import sys
libpath = Path(__file__).parent.parent
sys.path.append(str(libpath))
from adventop import IntCode

base = libpath.parent

def test_day2_1():
    inprog = [1,0,0,0,99]
    compy = IntCode(inprog)
    compy.run_to_completion()
    assert compy.work_prog == [2,0,0,0,99]


def test_day2_2():
    inprog = [2,3,0,3,99]
    compy = IntCode(inprog)
    compy.run_to_completion()
    assert compy.work_prog == [2,3,0,6,99]

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