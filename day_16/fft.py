from pathlib import Path
from itertools import cycle, repeat, chain

here = Path(__file__).parent.resolve()
EX0 = [1, 2, 3, 4, 5, 6, 7, 8]
EX1 = [int(x) for x in "80871224585914546619083218645595"]
EX2 = [int(x) for x in "19617804207202209144916044189917"]
EX3 = [int(x) for x in "69317163492948606335995924319873"]
with open(here / "input.txt", "r") as f:
    IN = [int(x) for x in f.readline()]

BASE_PATTERN = [0, 1, 0, -1]

def fft_element(signal, position):
    pattern = BASE_PATTERN[:]
    ff_pattern = cycle(chain.from_iterable(repeat(i, position) for i in pattern))
    # consume first element in pattern
    next(ff_pattern)
    return abs(sum(sig * pat for sig, pat in zip(signal, ff_pattern))) % 10

def fft_phase(signal):
    return [fft_element(signal, i + 1) for i in range(len(signal))]

def fft(signal, num_phases=100):
    for _ in range(num_phases):
        signal = fft_phase(signal)
    return signal

def part1(signal):
    numlist = fft(signal, num_phases=100)
    return "".join(str(i) for i in numlist[:8])

assert part1(EX1) == "24176176"
assert part1(EX2) == "73745418"
assert part1(EX3) == "52432133"
print(part1(IN))

def part2(numlist):
    offset = int("".join(str(x) for x in numlist[:7]))
    numlist = numlist * 10_000
    for _ in range(100):
        position = len(numlist) - 1
        total = 0
        while position >= offset:
            total += numlist[position]
            numlist[position] = abs(total) % 10
            position -= 1
    result = "".join(str(x) for x in numlist[offset:offset + 8])
    return result

print(part2(IN))
