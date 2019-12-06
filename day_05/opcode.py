def readlist(file="day_05/input.txt"):
    with open(file, "r") as f:
        return [int(char) for char in f.readline().split(",")]


def parse_instruction(instruction):
    sint = str(instruction).zfill(5)
    parm3 = bool(int(sint[0]))
    parm2 = bool(int(sint[1]))
    parm1 = bool(int(sint[2]))
    op = int(sint[-2:])
    return op, parm1, parm2, parm3


def opcoder():
    in_list = readlist()
    i = 0
    inputs = 0
    singleinput = 1

    def parmnum(parm, num):
        if parm:
            return num
        else:
            return in_list[num]

    while in_list[i] != 99:
        op, parm1, parm2, parm3 = parse_instruction(in_list[i])
        j = parmnum(parm1, i + 1)
        k = parmnum(parm2, i + 2)
        m = parmnum(parm3, i + 3)
        if op == 1:
            in_list[m] = in_list[j] + in_list[k]
            i += 4
        elif op == 2:
            in_list[m] = in_list[j] * in_list[k]
            i += 4
        elif op == 3:
            in_list[j] = singleinput
            inputs += 1
            i += 2
        elif op == 4:
            if in_list[j] != 0:
                print(in_list[j])
            i += 2
        else:
            raise (ValueError)
    assert inputs == 1
    return True


opcoder()


def opcoder2():
    in_list = readlist()
    i = 0
    inputs = 0
    singleinput = 5

    def parmnum(parm, num):
        if parm:
            return num
        else:
            return in_list[num]

    while in_list[i] != 99:
        op, parm1, parm2, parm3 = parse_instruction(in_list[i])
        j = parmnum(parm1, i + 1)
        k = parmnum(parm2, i + 2)
        m = parmnum(parm3, i + 3)
        if op == 1:
            in_list[m] = in_list[j] + in_list[k]
            i += 4
        elif op == 2:
            in_list[m] = in_list[j] * in_list[k]
            i += 4
        elif op == 3:
            in_list[j] = singleinput
            inputs += 1
            i += 2
        elif op == 4:
            print(in_list[j])
            i += 2
        elif op == 5:
            if in_list[j] != 0:
                i = in_list[k]
            else:
                i += 3
        elif op == 6:
            if in_list[j] == 0:
                i = in_list[k]
            else:
                i += 3
        elif op == 7:
            if in_list[j] < in_list[k]:
                in_list[m] = 1
            else:
                in_list[m] = 0
            i += 4
        elif op == 8:
            if in_list[j] == in_list[k]:
                in_list[m] = 1
            else:
                in_list[m] = 0
            i += 4
        else:
            raise (ValueError)
    assert inputs == 1
    return True


opcoder2()
