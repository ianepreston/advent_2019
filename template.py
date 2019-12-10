from pathlib import Path
import sys
here = Path(__file__).parent
base = here.parent / "adventlib"
sys.path.append(str(base))
from adventop import opcoder, read_program