total_fuel = 0
with open("input.txt", "r") as f:
    for line in f.readlines():
        num = int(line)
        total_fuel += (num // 3) - 2

print(total_fuel)


def calc_fuel(num):
    return (num // 3) - 2

def recursive_fuel(num):
    base = calc_fuel(num)
    if base <= 0:
        return 0
    else:
        return base + recursive_fuel(base)

total_fuel = 0
with open("input.txt", "r") as f:
    for line in f.readlines():
        num = int(line)
        total_fuel += recursive_fuel(num)
print(total_fuel)

