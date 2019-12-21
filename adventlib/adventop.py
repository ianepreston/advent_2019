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
            try:
                return self[num]
            except IndexError:
                return None

    def execute_op(self):
        if not self.running:
            raise Exception("No operations to execute, program has halted")
        op, parm1, parm2, parm3 = IntCode.parse_instruction(self[self.index])
        j, k, m = (
            self.parnum(parm, self.index + num)
            for parm, num in zip((parm1, parm2, parm3), range(1, 4))
        )
        if op == 1:
            self[m] = self[j] + self[k]
            self.index += 4
        elif op == 2:
            self[m] = self[j] * self[k]
            self.index += 4
        elif op == 3:
            self[j] = self.inputs[0]
            self.inputs = self.inputs[1:]
            self.index += 2
        elif op == 4:
            self.outputs = np.append(self.outputs, self[j])
            self.index += 2
        elif op == 5:
            if self[j] != 0:
                self.index = self[k]
            else:
                self.index += 3
        elif op == 6:
            if self[j] == 0:
                self.index = self[k]
            else:
                self.index += 3
        elif op == 7:
            if self[j] < self[k]:
                self[m] = 1
            else:
                self[m] = 0
            self.index += 4
        elif op == 8:
            if self[j] == self[k]:
                self[m] = 1
            else:
                self[m] = 0
            self.index += 4
        else:
            raise ValueError(f"invalid opcode provided: {op}")

    def receive_input(self, *args):
        self.inputs = np.append(self.inputs, args)
        return self

    def next_output(self):
        output_count = len(self.outputs)
        while self.running:
            self.execute_op()
            if len(self.outputs) > output_count:
                return self.outputs[-1]
        return None

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

