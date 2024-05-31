class Uniciclo:
    def __init__(self):
        self.pc = 0  # Program Counter
        self.registers = [0] * 32  # 32 registros
        self.memory = [0] * 1024  # Memoria de 1 KB
        self.instructions = []  # Lista de instrucciones cargadas

    def load_program(self, program):
        self.instructions = program

    def fetch(self):
        if self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            self.pc += 1
            return instruction
        return None

    def decode(self, instruction):
        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x07
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F
        imm = instruction >> 20  # Para instrucciones tipo I
        return opcode, rd, funct3, rs1, rs2, funct7, imm

    def execute(self, opcode, rd, funct3, rs1, rs2, funct7, imm):
        try:
            if opcode == 0x33:  # Tipo R
                if funct3 == 0x0:  # ADD o SUB
                    if funct7 == 0x00:  # ADD
                        self.registers[rd] = self.registers[rs1] + self.registers[rs2]
                    elif funct7 == 0x20:  # SUB
                        self.registers[rd] = self.registers[rs1] - self.registers[rs2]
                elif funct3 == 0x7:  # AND
                    self.registers[rd] = self.registers[rs1] & self.registers[rs2]
                elif funct3 == 0x6:  # OR
                    self.registers[rd] = self.registers[rs1] | self.registers[rs2]
            elif opcode == 0x13:  # Tipo I
                if funct3 == 0x0:  # ADDI
                    self.registers[rd] = self.registers[rs1] + imm
                elif funct3 == 0x6:  # ORI
                    self.registers[rd] = self.registers[rs1] | imm
                elif funct3 == 0x7:  # ANDI
                    self.registers[rd] = self.registers[rs1] & imm
            elif opcode == 0x03:  # Tipo L, Load
                if funct3 == 0x2:  # LW
                    self.registers[rd] = self.memory[self.registers[rs1] + imm]
            elif opcode == 0x23:  # Tipo S, Store
                if funct3 == 0x2:  # SW
                    self.memory[self.registers[rs1] + imm] = self.registers[rs2]
            elif opcode == 0x63:  # Tipo B, Branch
                if funct3 == 0x0:  # BEQ
                    if self.registers[rs1] == self.registers[rs2]:
                        self.pc += imm
                elif funct3 == 0x1:  # BNE
                    if self.registers[rs1] != self.registers[rs2]:
                        self.pc += imm
            elif opcode == 0x37:  # LUI
                self.registers[rd] = imm << 12
            elif opcode == 0x17:  # AUIPC
                self.registers[rd] = self.pc + (imm << 12)
        except Exception as e:
            print(f"Error executing instruction: {e}")

    def run(self):
        output = ""
        while self.pc < len(self.instructions):
            instruction = self.fetch()
            if instruction is None:
                break
            opcode, rd, funct3, rs1, rs2, funct7, imm = self.decode(instruction)
            self.execute(opcode, rd, funct3, rs1, rs2, funct7, imm)
            output += f"PC: {self.pc}, Instruction: {instruction}, Registers: {self.registers}\n"
        return output

    def step(self):
        output = ""
        instruction = self.fetch()
        if instruction:
            opcode, rd, funct3, rs1, rs2, funct7, imm = self.decode(instruction)
            self.execute(opcode, rd, funct3, rs1, rs2, funct7, imm)
            output += f"PC: {self.pc}, Instruction: {instruction}, Registers: {self.registers}\n"
        return output

    def display_memory(self):
        memory_content = "Memory Content:\n"
        for i in range(len(self.memory)):
            if self.memory[i] != 0:
                memory_content += f"Address {i}: {self.memory[i]}\n"
        return memory_content
