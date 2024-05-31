class Registers:
    def __init__(self):
        self.registers = [0] * 32

    def read(self, reg_num):
        return self.registers[reg_num]

    def write(self, reg_num, value):
        self.registers[reg_num] = value
