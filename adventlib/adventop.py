"""Op code manager for advent of code"""
from pathlib import Path

class IntCode:
    """Might as well build this right finally"""
    def __init__(self, prog):
        if isinstance(prog, str) or isinstance(prog, Path):
            with open(prog, "r") as f:
                self.input_prog = [int(x) for x in f.readline().rstrip().split(",")]
        else:
            self.input_prog = prog
        self.work_prog = self.input_prog[:] # make a copy so we can restart if necessary
        self.index = 0
        self.inputs = list()
        self.outputs = list()

    
    @staticmethod
    def parse_instruction(instruction):
        sint = str(instruction).zfill(5)
        parm3 = bool(int(sint[0]))
        parm2 = bool(int(sint[1]))
        parm1 = bool(int(sint[2]))
        op = int(sint[-2:])
        return op, parm1, parm2, parm3
    
    def parnum(self, parm, num):
        """Depending on parameter mode return an index or a number"""
        if parm:
            return num
        else:
            return self.work_prog[num]
    
    def execute_op(self):
        op, parm1, parm2, parm3 = IntCode.parse_instruction(self.work_prog[self.index])
        j = self.parnum(parm1, self.index + 1)
        k = self.parnum(parm2, self.index + 2)
        m = self.parnum(parm3, self.index + 3)
        if op == 1:
            self.work_prog[m] = self.work_prog[j] + self.work_prog[k]
            self.index += 4
            return (True, None)
        elif op == 2:
            self.work_prog[m] = self.work_prog[j] * self.work_prog[k]
            self.index += 4
            return (True, None)
        elif op == 3:
            self.work_prog[j] = self.inputs.pop(0)
            self.index += 2
            return (True, None)
        elif op == 4:
            self.outputs.append(self.work_prog[j])
            self.index += 2
            return (True, self.work_prog[j])
        elif op == 5:
            if self.work_prog[j] != 0:
                self.index = self.work_prog[k]
            else:
                self.index += 3
            return (True, None)
        elif op == 6:
            if self.work_prog[j] == 0:
                self.index = self.work_prog[k]
            else:
                self.index += 3
            return (True, None)
        elif op == 7:
            if self.work_prog[j] < self.work_prog[k]:
                self.work_prog[m] = 1
            else:
                self.work_prog[m] = 0
            self.index += 4
            return (True, None)
        elif op == 8:
            if self.work_prog[j] == self.work_prog[k]:
                self.work_prog[m] = 1
            else:
                self.work_prog[m] = 0
            self.index += 4
        elif self.work_prog[self.index] == 99:
            return (False, None)
        else:
            raise ValueError
    
    def receive_input(self, *args):
        for arg in args:
            self.inputs.append(arg)
        return True
    
    def next_output(self):
        while self.work_prog[self.index] != 99:
            passfail, result = self.execute_op()
            if result is not None:
                return result
    
    def run_to_completion(self):
        while self.work_prog[self.index] != 99:
            self.execute_op()
        return self.outputs



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

