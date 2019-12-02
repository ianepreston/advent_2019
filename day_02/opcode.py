def readlist(file="day_02/input.txt"):
    with open(file, "r") as f:
        return [int(char) for char in f.readline().split(",")]


def opcoder(in_list, replacement=None):
    i = 0
    work_list = in_list[:]
    if replacement is not None:
        work_list[1], work_list[2] = replacement
    while work_list[i] != 99:
        j = work_list[i + 1]
        k = work_list[i + 2]
        m = work_list[i + 3]
        if work_list[i] == 1:
            work_list[m] = work_list[j] + work_list[k]
        elif work_list[i] == 2:
            work_list[m] = work_list[j] * work_list[k]
        else:
            raise (ValueError)
        i += 4
    return work_list


assert opcoder([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
assert opcoder([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
assert opcoder([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
assert opcoder([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]

print(opcoder(readlist(), replacement=(12, 2))[0])


def opcoder2():
    base = readlist()
    for noun in range(100):
        for verb in range(100):
            if opcoder(base, replacement=(noun, verb))[0] == 19690720:
                return 100 * noun + verb


print(opcoder2())

