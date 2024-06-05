class Uniciclo:
    def __init__(self):
        self.memory = bytearray(1024)  # 1KB of memory
        self.registers = [0] * 32
        self.pc = 0
        self.cycle = 0

    def load_program(self, program):
        self.pc = 0
        for i, instruction in enumerate(program):
            self.memory[i * 4:(i + 1) * 4] = instruction.to_bytes(4, byteorder='little')

    def run(self):
        output = ""
        while self.pc < len(self.memory):
            output += self.step()
        return output

    def step(self):
        instruction = int.from_bytes(self.memory[self.pc:self.pc+4], 'little')
        self.pc += 4
        self.cycle += 1

        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x7
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F

        if opcode == 0x03 and funct3 == 0x2:  # lw
            imm = instruction >> 20
            address = self.registers[rs1] + imm
            self.registers[rd] = int.from_bytes(self.memory[address:address+4], 'little')
        elif opcode == 0x23 and funct3 == 0x2:  # sw
            imm = ((instruction >> 25) << 5) | ((instruction >> 7) & 0x1F)
            address = self.registers[rs1] + imm
            self.memory[address:address+4] = self.registers[rs2].to_bytes(4, 'little')
        elif opcode == 0x33:  # R-type (add, sub, mul)
            if funct3 == 0x0:
                if funct7 == 0x00:  # add
                    self.registers[rd] = self.registers[rs1] + self.registers[rs2]
                elif funct7 == 0x20:  # sub
                    self.registers[rd] = self.registers[rs1] - self.registers[rs2]
                elif funct7 == 0x01:  # mul
                    self.registers[rd] = self.registers[rs1] * self.registers[rs2]

        return f"PC: 0x{self.pc:08X}, Cycle: {self.cycle}, Instruction: 0x{instruction:08X}\n"
