def solver(fuel_func):
    total_fuel = 0
    with open("input.txt", "r") as f:
        for line in f.readlines():
            total_fuel += fuel_func(int(line))
    return total_fuel


def calc_fuel(num):
    return (num // 3) - 2


print(solver(calc_fuel))


def recursive_fuel(num):
    base = calc_fuel(num)
    if base <= 0:
        return 0
    else:
        return base + recursive_fuel(base)


print(solver(recursive_fuel))
