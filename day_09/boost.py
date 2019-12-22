from pathlib import Path
import sys

here = Path(__file__).parent.resolve()
base = here.parent / "adventlib"
sys.path.append(str(base))
from adventop import IntCode

EX1 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
EX2 = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
EX3 = [104, 1125899906842624, 99]
IN = here / "input.txt"

int_ex1 = IntCode(EX1)
assert list(int_ex1.run_to_completion()) == EX1

int_ex2 = IntCode(EX2)
assert int_ex2.run_to_completion()[0] == 1219070632396864
int_ex3 = IntCode(EX3)
assert int_ex3.run_to_completion()[0] == EX3[1]
boost_int = IntCode(IN)
boost_int.receive_input(1)
print(boost_int.run_to_completion())

boost_int_part2 = IntCode(IN)
boost_int_part2.receive_input(2)
print(boost_int_part2.run_to_completion())