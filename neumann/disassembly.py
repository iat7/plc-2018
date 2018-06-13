import numpy as np
import sys

COMMANDS = ["mov", "add", "sub", "pop", "push", "call", "funcb", "funce", "term", "jump", "rjgz", "print", "read", "putstr" ]
ARGUMENTS_NUM = [2, 2, 2, 0, 1, 1, 1, 0, 0, 1, 2, 1, 1, 1]
INSTRUCTION_SIZE = 5


def get_argument_str(arg, access):
    return "*" * access + str(arg)


def get_static_string(static_data, num):
    offset = static_data[num]
    strlen = static_data[offset]
    str = ""
    for i in range(strlen):
        str += chr(static_data[offset + i + 1])
    return str

if len(sys.argv) < 1:
    print "Specify binary filename"

if len(sys.argv) < 2:
    print "Specify output filename"

output = open(sys.argv[2], "w")
code = np.fromfile(sys.argv[1], dtype=np.int32)
code_length = code[0]
for i in range(0, code_length / INSTRUCTION_SIZE):
    instruction = code[1 + i * INSTRUCTION_SIZE]
    arg1_a = code[1 + i * INSTRUCTION_SIZE + 1]
    arg1 = code[1 + i * INSTRUCTION_SIZE + 2]
    arg2_a = code[1 + i * INSTRUCTION_SIZE + 3]
    arg2 = code[1 + i * INSTRUCTION_SIZE + 4]
    command_str = COMMANDS[instruction]
    if command_str == "putstr":
        command_str += " " + get_static_string(code[code_length + 1:], arg1)
    else:
        if ARGUMENTS_NUM[instruction] >= 1:
            command_str += " " + get_argument_str(arg1, arg1_a)
        if ARGUMENTS_NUM[instruction] >= 2:
            command_str += " " + get_argument_str(arg2, arg2_a)
    output.write(command_str + "\n")

output.close()