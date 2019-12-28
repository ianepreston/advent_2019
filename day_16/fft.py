from pathlib import Path

here = Path(__file__).parent.resolve()
EX1 = [int(x) for x in "80871224585914546619083218645595"]
EX2 = [int(x) for x in "19617804207202209144916044189917"]
EX3 = [int(x) for x in "69317163492948606335995924319873"]
with open(here / "input.txt", "r") as f:
    IN = [int(x) for x in f.readline()]

