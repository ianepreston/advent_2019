from pathlib import Path
import sys
here = Path(__file__).parent.resolve()
base = here.parent / "adventlib"
sys.path.append(str(base))
from adventop import IntCode 

robot = IntCode(here / "input.txt")