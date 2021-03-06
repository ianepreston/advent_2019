"""Op code manager for advent of code"""
from pathlib import Path
import numpy as np


class IntCode:
    """Might as well build this right finally"""

    def __init__(self, prog):
        if isinstance(prog, str) or isinstance(prog, Path):
            with open(prog, "r") as f:
                self.input_prog = np.array(
                    [int(x) for x in f.readline().rstrip().split(",")], dtype="int64"
                )
        else:
            self.input_prog = np.array(prog, dtype="int64")
        # make a copy so we can restart if necessary
        self.work_prog = self.input_prog.copy()
        self.index = 0
        self.relative_base = 0
        self.inputs = np.array([], dtype="int64")
        self.outputs = np.array([], dtype="int64")

    def __getitem__(self, key):
        if key < 0:
            raise IndexError("negative indexes are not supported")
        try:
            val = self.work_prog[key]
        except IndexError:
            self.work_prog.resize(key + 1, refcheck=False)
            val = self.work_prog[key]
        return val

    def __setitem__(self, key, value):
        if key < 0:
            raise IndexError("negative indexes are not supported")
        try:
            self.work_prog[key] = value
        except IndexError:
            self.work_prog.resize(key + 1, refcheck=False)
            self.work_prog[key] = value
        return value

    def parnum(self, parm, num):
        """Depending on parameter mode return an index or a number"""
        if parm == 0:
            return self[num]
        elif parm == 1:
            return num
        elif parm == 2:
            return self.relative_base + self[num]
        # elif parm == 22:
        # return self[self.relative_base + self[num]]
        else:
            raise ValueError(f"invalid parameter: {parm}")

    def parse_op(self, instruction):
        """
        First two digits are the opcode
        next are the parameter modes for the remaining parameters
        parameter mode 0 is position mode, return index for that parameter
        parameter mode 1 is immediate mode, return that parameter
        parameter mode 2 is relative mode, return the index in the relative offset + that parameter
        parameters that an instruction writes to will never be in immediate mode - I guess we default back to position?
        """
        op = instruction % 100
        instruction = instruction // 100
        parameter_modes = list()
        for _ in range(3):
            parameter_modes.append(instruction % 10)
            instruction = instruction // 10
        if op in (1, 2, 7, 8):
            if parameter_modes[2] == 1:
                parameter_modes[2] = 0
            # elif parameter_modes[2] == 2:
            # parameter_modes[2] =22

        elif op == 3:
            if parameter_modes[0] == 1:
                parameter_modes[0] = 0
            # elif parameter_modes[0] == 2:
            # parameter_modes[0] = 22
        parameters = [
            self.parnum(parm, self.index + num)
            for num, parm in enumerate(parameter_modes, 1)
        ]
        return [op] + parameters

    def execute_op(self):
        if not self.running:
            raise Exception("No operations to execute, program has halted")
        op, parm1, parm2, parm3 = self.parse_op(self[self.index])
        if op == 1:
            self[parm3] = self[parm1] + self[parm2]
            self.index += 4
        elif op == 2:
            self[parm3] = self[parm1] * self[parm2]
            self.index += 4
        elif op == 3:
            self[parm1] = self.inputs[0]
            self.inputs = self.inputs[1:]
            self.index += 2
        elif op == 4:
            self.outputs = np.append(self.outputs, self[parm1])
            self.index += 2
        elif op == 5:
            if self[parm1] != 0:
                self.index = self[parm2]
            else:
                self.index += 3
        elif op == 6:
            if self[parm1] == 0:
                self.index = self[parm2]
            else:
                self.index += 3
        elif op == 7:
            if self[parm1] < self[parm2]:
                self[parm3] = 1
            else:
                self[parm3] = 0
            self.index += 4
        elif op == 8:
            if self[parm1] == self[parm2]:
                self[parm3] = 1
            else:
                self[parm3] = 0
            self.index += 4
        elif op == 9:
            self.relative_base += self[parm1]
            self.index += 2
        else:
            raise ValueError(f"invalid opcode provided: {op}")

    def receive_input(self, *args):
        self.inputs = np.append(self.inputs, args)
        return self

    def next_output(self):
        op = 0
        while op != 4 and self.running:
            op, *_ = self.parse_op(self[self.index])
            self.execute_op()
        if op == 4:
            return self.outputs[-1]
        else:
            return None
    
    def run_to_next_input(self):
        op = 0
        while op != 3 and self.running:
            op, *_ = self.parse_op(self[self.index])
            self.execute_op()
    
    def run_to_next_io(self):
        op, *_ = self.parse_op(self[self.index])
        while op != 3 and op != 4 and self.running:
            self.execute_op()
            op, *_ = self.parse_op(self[self.index])
        return op

    def run_to_completion(self):
        while self.running:
            self.execute_op()
        return self.outputs

    @property
    def running(self):
        return self[self.index] != 99


def read_program(file):
    """Deprecated"""
    with open(file, "r") as f:
        return [int(x) for x in f.readline().rstrip().split(",")]


def parse_instruction(instruction):
    """Deprecated"""
    sint = str(instruction).zfill(5)
    parm3 = bool(int(sint[0]))
    parm2 = bool(int(sint[1]))
    parm1 = bool(int(sint[2]))
    op = int(sint[-2:])
    return op, parm1, parm2, parm3


def opcoder(in_list, args):
    """Deprecated"""
    work_list = in_list[:]  # don't modify your program
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
