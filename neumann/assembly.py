import numpy as np
import sys

COMMAND_CODES = { "mov": 0, "add": 1, "sub": 2, "pop": 3, "push": 4, "call": 5, "funcb": 6, "funce": 7, "term": 8, "jump": 9, "rjgz": 10, "print": 11, "read": 12, "putstr": 13 }
REGISTRIES = {"ip": 0, "sp": 1, "rv": 2, "r1": 3, "r2": 4, "r3": 5, "r4": 6, "r5": 7}

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def get_arg_value(arg):
    if REGISTRIES.has_key(arg):
        return REGISTRIES[arg]
    elif represents_int(arg):
        return int(arg)
    else:
        print "Invalid argument " + arg

def get_arg_with_access_type(arg):
    access_level = 0
    while arg[access_level] == "*":
        access_level += 1
    return access_level, get_arg_value(arg[access_level:])


strarray = []


def generate_statics():
    total_size = len(strarray)
    for str in strarray:
        total_size += len(str) + 1
    data = np.zeros(total_size, dtype=np.int32)
    current_offset = len(strarray)
    for i in range(len(strarray)):
        str = strarray[i]
        data[i] = current_offset
        data[current_offset] = len(str)
        current_offset += 1
        for c in str:
            code = ord(c)
            data[current_offset] = code
            current_offset += 1
    return data


def generate_bytecode(source_filename):
    bytecode = []
    with open(source_filename) as f:
        for line in f.readlines():
            tokens_high_level = line.strip().split(' ', 1)
            if tokens_high_level[0] == "putstr":
                strarray.append(tokens_high_level[1])
                bytecode.append(COMMAND_CODES["putstr"])
                bytecode.append(0)
                bytecode.append(len(strarray) - 1)
                bytecode.append(0)
                bytecode.append(0)
                continue

            tokens = line.strip().split(' ')
            if not COMMAND_CODES.has_key(tokens[0]):
                print "invalid command " + tokens[0]
            code = COMMAND_CODES[tokens[0]]
            first_arg = 0
            first_at = 0
            second_arg = 0
            second_at = 0
            if len(tokens) > 1:
                first_at, first_arg = get_arg_with_access_type(tokens[1])
            if len(tokens) > 2:
                second_at, second_arg = get_arg_with_access_type(tokens[2])
            bytecode.append(code)
            bytecode.append(first_at)
            bytecode.append(first_arg)
            bytecode.append(second_at)
            bytecode.append(second_arg)
    return np.array( bytecode, dtype=np.int32 )

if len(sys.argv) < 1:
    print "Specify source filename"

if len(sys.argv) < 2:
    print "Specify output filename"

bytecode = generate_bytecode(sys.argv[1])
bytecode_size = len(bytecode)
static_data = generate_statics()
total_result = np.concatenate([np.array([bytecode_size], dtype=np.int32), bytecode, static_data])
total_result.tofile(sys.argv[2])