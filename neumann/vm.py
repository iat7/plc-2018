import numpy as np
import sys

INSTRUCTION_SIZE = 5
NUMBER_OF_REGISTERS = 8

COMMAND_MOV = 0
COMMAND_ADD = 1
COMMAND_SUB = 2
COMMAND_POP = 3
COMMAND_PUSH = 4
COMMAND_CALL = 5
COMMAND_FUNCB = 6
COMMAND_FUNCE = 7
COMMAND_TERMINATE = 8
COMMAND_JUMP = 9
COMMAND_RJGZ = 10
COMMAND_PRINT = 11
COMMAND_READ = 12
COMMAND_PUTSTR = 13

IP_INDEX = 0
SP_INDEX = 1

class Memory:
    def __init__(self, memory_size):
        self.memory = np.zeros(memory_size, dtype=np.int32)

    def write_word(self, address, word ):
        self.memory[address] = word

    def read_word(self, address):
        return self.memory[address]


class Interpreter:
    def __init__(self, memory, static_offset):
        self.memory = memory
        self.static_offset = static_offset
        self.function_startpoints = {}
        self.reading_function = False

    def ip_value(self):
        return self.memory.read_word(IP_INDEX)

    def ip_address(self):
        return IP_INDEX

    def sp_value(self):
        return self.memory.read_word(SP_INDEX)

    def sp_address(self):
        return SP_INDEX

    def get_value(self, value, access):
        for i in range(access):
            value = self.memory.read_word(value)
        return value

    def next_command(self):
        self.memory.write_word(self.ip_address(),self.memory.read_word(self.ip_address()) + INSTRUCTION_SIZE)

    def mov(self, dest, dest_access, src, src_access):
        dest_address = self.get_value(dest, dest_access)
        src_value = self.get_value(src, src_access)
        self.memory.write_word(dest_address, src_value)
        self.next_command()

    def add(self, dest, dest_access, addition, addition_access, next_com=True):
        dest_address = self.get_value(dest, dest_access)
        addition_value = self.get_value(addition, addition_access)
        self.memory.write_word(dest_address, self.memory.read_word(dest) + addition_value)
        if next_com:
            self.next_command()

    def sub(self, dest, dest_access, sub, sub_access, next_com=True):
        dest_address = self.get_value(dest, dest_access)
        sub_value = self.get_value(sub, sub_access)
        sub_result = self.memory.read_word(dest) - sub_value
        self.memory.write_word(dest_address, sub_result)
        if next_com:
            self.next_command()
    
    def jump(self, dest, dest_access):
        instruction_number = self.get_value(dest, dest_access)
        self.memory.write_word(self.ip_address(), instruction_number)

    def rjgz(self, val, val_access, dest, dest_access):
        value = self.get_value(val, val_access)
        if value > 0:
            addr_diff = self.get_value(dest, dest_access)
            self.add(IP_INDEX, 0, addr_diff * INSTRUCTION_SIZE, 0, False)
        else:
            self.next_command()

    def pop(self):
        self.add(self.sp_address(), 0, 1, 0, False)
        self.next_command()

    def push(self, val, val_access, next_com=True):
        self.sub(self.sp_address(), 0, 1, 0, False)
        self.memory.write_word(self.sp_value(), self.get_value(val, val_access))
        if next_com:
            self.next_command()
    
    def call(self, val, val_access):
        value = self.get_value(val, val_access)
        self.push(self.ip_value() + INSTRUCTION_SIZE, 0, False)
        self.memory.write_word(self.ip_address(), self.function_startpoints[value])
    
    def func_begin(self, number, number_access):
        num = self.get_value(number, number_access)
        self.function_startpoints[num] = self.ip_value() + INSTRUCTION_SIZE
        self.reading_function = True
        self.next_command()
    
    def func_end(self):
        self.reading_function = False
        self.next_command()

    def print_(self, val, val_access):
        value = self.get_value(val, val_access)
        print value
        self.next_command()

    def read(self, dest, dest_access):
        address = self.get_value(dest, dest_access)
        read_value = int(input())
        self.memory.write_word(address, read_value)
        self.next_command()

    def print_static_string(self, arg):
        static_address = self.memory.read_word(self.static_offset + arg)
        strln = self.memory.read_word(self.static_offset + static_address)
        str = ""
        for i in range(strln):
            str += chr(self.memory.read_word(self.static_offset + static_address + i + 1))
        print str
        self.next_command()

    def interpret_next_command(self):
        instruction = self.get_value(self.ip_value(), 1)
        first_arg_access = self.get_value(self.ip_value() + 1, 1)
        argument1 = self.get_value(self.ip_value() + 2, 1)
        second_arg_access = self.get_value(self.ip_value() + 3 , 1)
        argument2 = self.get_value(self.ip_value() + 4, 1)

        if self.reading_function and not instruction == COMMAND_FUNCE:
            self.next_command()
            return True

        if instruction == COMMAND_MOV:
            self.mov(argument1, first_arg_access, argument2, second_arg_access)
            return True
        elif instruction == COMMAND_ADD:
            self.add(argument1, first_arg_access, argument2, second_arg_access)
            return True
        elif instruction == COMMAND_CALL:
            self.call(argument1, first_arg_access)
            return True
        elif instruction == COMMAND_SUB:
            self.sub(argument1, first_arg_access, argument2, second_arg_access)
            return True
        elif instruction == COMMAND_POP:
            self.pop()
            return True
        elif instruction == COMMAND_PUSH:
            self.push(argument1, first_arg_access)
            return True
        elif instruction == COMMAND_FUNCB:
            self.func_begin(argument1, first_arg_access)
            return True
        elif instruction == COMMAND_FUNCE:
            self.func_end()
            return True
        elif instruction == COMMAND_JUMP:
            self.jump(argument1, first_arg_access)
            return True
        elif instruction == COMMAND_RJGZ:
            self.rjgz(argument1, first_arg_access, argument2, second_arg_access)
            return True
        elif instruction == COMMAND_TERMINATE:
            return False
        elif instruction == COMMAND_PRINT:
            self.print_(argument1, first_arg_access)
            return True
        elif instruction == COMMAND_READ:
            self.read(argument1, first_arg_access)
            return True
        elif instruction == COMMAND_PUTSTR:
            self.print_static_string(argument1)
            return True

    def run_execution(self):
        while self.interpret_next_command():
            pass


if len(sys.argv) < 2:
    print "Specify binary filename"

MEMORY_SIZE = 10000000
memory = Memory(MEMORY_SIZE)
memory.write_word(IP_INDEX, NUMBER_OF_REGISTERS)
memory.write_word(SP_INDEX, MEMORY_SIZE)
code = np.fromfile(sys.argv[1], dtype=np.int32)
code_size = code[0]
for i in range(1, len(code)):
    memory.write_word(NUMBER_OF_REGISTERS + i - 1, code[i])
interpreter = Interpreter(memory, NUMBER_OF_REGISTERS + code_size)
interpreter.run_execution()