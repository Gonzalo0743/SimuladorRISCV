class PipelineStage:
    def __init__(self):
        self.instruction = None
        self.pc = None

class Pipeline:
    def __init__(self):
        self.IF = PipelineStage()
        self.ID = PipelineStage()
        self.EX = PipelineStage()
        self.MEM = PipelineStage()
        self.WB = PipelineStage()

class Segmentado_Stalls:
    def __init__(self):
        self.memory = bytearray(1024)  # 1KB de memoria
        self.registers = [0] * 32
        self.pc = 0
        self.cycle = 0
        self.pipeline = Pipeline()
        self.stalled = False

    def load_program(self, program):
        self.pc = 0
        for i, instruction in enumerate(program):
            self.memory[i * 4:(i + 1) * 4] = instruction.to_bytes(4, byteorder='little')

    def run(self):
        output = ""
        while self.pc < len(self.memory) or self.pipeline.IF.instruction or self.pipeline.ID.instruction or self.pipeline.EX.instruction or self.pipeline.MEM.instruction or self.pipeline.WB.instruction:
            output += self.step()
        return output

    def step(self):
        self.cycle += 1
        output = f"Cycle: {self.cycle}\n"

        # Write Back (WB)
        if self.pipeline.WB.instruction:
            self.write_back()

        # Memory Access (MEM)
        if self.pipeline.MEM.instruction:
            self.memory_access()

        # Execute (EX)
        if self.pipeline.EX.instruction:
            self.execute()

        # Instruction Decode (ID)
        if self.pipeline.ID.instruction:
            self.decode()

        # Instruction Fetch (IF)
        if not self.stalled:
            self.fetch()

        return output

    def fetch(self):
        if self.pc < len(self.memory):
            self.pipeline.IF.instruction = int.from_bytes(self.memory[self.pc:self.pc+4], 'little')
            self.pipeline.IF.pc = self.pc
            self.pc += 4
        else:
            self.pipeline.IF.instruction = None

    def decode(self):
        instruction = self.pipeline.IF.instruction
        if instruction is not None:
            self.pipeline.ID.instruction = instruction
            self.pipeline.ID.pc = self.pipeline.IF.pc

            opcode = instruction & 0x7F
            funct3 = (instruction >> 12) & 0x7
            rs1 = (instruction >> 15) & 0x1F
            rs2 = (instruction >> 20) & 0x1F
            rd = (instruction >> 7) & 0x1F
            funct7 = (instruction >> 25) & 0x7F

            if opcode == 0x03 and funct3 == 0x2:  # lw
                imm = instruction >> 20
                self.stall_if_needed(rs1)
            elif opcode == 0x23 and funct3 == 0x2:  # sw
                imm = ((instruction >> 25) << 5) | ((instruction >> 7) & 0x1F)
                self.stall_if_needed(rs1)
            elif opcode == 0x33:  # R-type (add, sub, mul)
                if funct3 == 0x0:
                    self.stall_if_needed(rs1, rs2)

    def execute(self):
        instruction = self.pipeline.ID.instruction
        if instruction is not None:
            self.pipeline.EX.instruction = instruction
            self.pipeline.EX.pc = self.pipeline.ID.pc

            opcode = instruction & 0x7F
            rd = (instruction >> 7) & 0x1F
            funct3 = (instruction >> 12) & 0x7
            rs1 = (instruction >> 15) & 0x1F
            rs2 = (instruction >> 20) & 0x1F
            funct7 = (instruction >> 25) & 0x7F

            if opcode == 0x33:  # R-type (add, sub, mul)
                if funct3 == 0x0:
                    if funct7 == 0x00:  # add
                        self.pipeline.EX.result = self.registers[rs1] + self.registers[rs2]
                    elif funct7 == 0x20:  # sub
                        self.pipeline.EX.result = self.registers[rs1] - self.registers[rs2]
                    elif funct7 == 0x01:  # mul
                        self.pipeline.EX.result = self.registers[rs1] * self.registers[rs2]

    def memory_access(self):
        instruction = self.pipeline.EX.instruction
        if instruction is not None:
            self.pipeline.MEM.instruction = instruction
            self.pipeline.MEM.pc = self.pipeline.EX.pc

            opcode = instruction & 0x7F
            rd = (instruction >> 7) & 0x1F
            funct3 = (instruction >> 12) & 0x7
            rs1 = (instruction >> 15) & 0x1F
            rs2 = (instruction >> 20) & 0x1F
            funct7 = (instruction >> 25) & 0x7F

            if opcode == 0x03 and funct3 == 0x2:  # lw
                imm = instruction >> 20
                address = self.registers[rs1] + imm
                self.pipeline.MEM.result = int.from_bytes(self.memory[address:address+4], 'little')
            elif opcode == 0x23 and funct3 == 0x2:  # sw
                imm = ((instruction >> 25) << 5) | ((instruction >> 7) & 0x1F)
                address = self.registers[rs1] + imm
                self.memory[address:address+4] = self.registers[rs2].to_bytes(4, 'little')

    def write_back(self):
        instruction = self.pipeline.MEM.instruction
        if instruction is not None:
            self.pipeline.WB.instruction = instruction
            self.pipeline.WB.pc = self.pipeline.MEM.pc

            opcode = instruction & 0x7F
            rd = (instruction >> 7) & 0x1F
            funct3 = (instruction >> 12) & 0x7
            rs1 = (instruction >> 15) & 0x1F
            rs2 = (instruction >> 20) & 0x1F
            funct7 = (instruction >> 25) & 0x7F

            if opcode == 0x03 and funct3 == 0x2:  # lw
                self.registers[rd] = self.pipeline.MEM.result
            elif opcode == 0x33:  # R-type (add, sub, mul)
                self.registers[rd] = self.pipeline.EX.result

    def stall_if_needed(self, *rs):
        # Si alguna de las instrucciones en las etapas posteriores usa alguno de estos registros, introducir un stall
        for r in rs:
            if self.pipeline.EX.instruction and r in [self.pipeline.EX.instruction >> 7 & 0x1F]:
                self.stalled = True
                return
            if self.pipeline.MEM.instruction and r in [self.pipeline.MEM.instruction >> 7 & 0x1F]:
                self.stalled = True
                return
        self.stalled = False
