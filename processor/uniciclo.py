class Uniciclo:
    def __init__(self):
        self.memory = bytearray(1024)  # 1KB de memoria
        self.registers = [0] * 32
        self.pc = 0
        self.cycle = 0
        self.program = []

    def load_program(self, program):
        self.program = program
        self.pc = 0
        self.cycle = 0

    def run(self):
        output = ""
        while self.pc < len(self.program) * 4:
            output += self.step()
        return output

    def step(self):
        if self.pc >= len(self.program) * 4:
            return "End of program\n"

        instruction = self.program[self.pc // 4]
        self.execute(instruction)
        self.pc += 4
        self.cycle += 1

        return f"Executed instruction 0x{instruction:08X} at PC 0x{self.pc:08X}\n"

    def execute(self, instruction):
        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x7
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F
        imm = instruction >> 20

        if opcode == 0x13:  # ADDI
            self.registers[rd] = self.registers[rs1] + imm
        elif opcode == 0x33:  # ADD
            self.registers[rd] = self.registers[rs1] + self.registers[rs2]
        elif opcode == 0x23:  # SW
            address = self.registers[rs1] + (imm >> 5)
            value = self.registers[rs2]
            self.memory[address:address+4] = value.to_bytes(4, byteorder='little')
        elif opcode == 0x63:  # BEQ
            if self.registers[rs1] == self.registers[rs2]:
                self.pc += (imm << 1) - 4  # Ajustamos porque se incrementa después
