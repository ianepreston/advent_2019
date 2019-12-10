"""Op code manager for advent of code"""
def read_program(file):
    with open(file, "r") as f:
        return [int(x) for x in f.readline().rstrip().split(",")]

def parse_instruction(instruction):
    sint = str(instruction).zfill(5)
    parm3 = bool(int(sint[0]))
    parm2 = bool(int(sint[1]))
    parm1 = bool(int(sint[2]))
    op = int(sint[-2:])
    return op, parm1, parm2, parm3


def opcoder(in_list, args):
    """Pretend you're a very simple computer"""
    work_list = in_list[:] # don't modify your program
    i = 0
    results = list()

    def parmnum(parm, num):
        if parm:
            return num
        else:
            return work_list[num]

    while work_list[i] != 99:
        op, parm1, parm2, parm3 = parse_instruction(work_list[i])
        j = parmnum(parm1, i + 1)
        k = parmnum(parm2, i + 2)
        m = parmnum(parm3, i + 3)
        if op == 1:
            work_list[m] = work_list[j] + work_list[k]
            i += 4
        elif op == 2:
            work_list[m] = work_list[j] * work_list[k]
            i += 4
        elif op == 3:
            work_list[j] = args.pop(0)
            i += 2
        elif op == 4:
            results.append(work_list[j])
            i += 2
        elif op == 5:
            if work_list[j] != 0:
                i = work_list[k]
            else:
                i += 3
        elif op == 6:
            if work_list[j] == 0:
                i = work_list[k]
            else:
                i += 3
        elif op == 7:
            if work_list[j] < work_list[k]:
                work_list[m] = 1
            else:
                work_list[m] = 0
            i += 4
        elif op == 8:
            if work_list[j] == work_list[k]:
                work_list[m] = 1
            else:
                work_list[m] = 0
            i += 4
        else:
            raise (ValueError)
    return results

