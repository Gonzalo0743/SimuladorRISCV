class PipelinedRegister:
    def __init__(self):
        self.instruction = 0
        self.pc = 0
        self.valid = False
        self.rd = 0
        self.rs1 = 0
        self.rs2 = 0
        self.funct3 = 0
        self.funct7 = 0
        self.imm = 0
        self.opcode = 0
        self.alu_result = 0

class Segmentado_Adelantamiento:
    def __init__(self):
        self.memory = bytearray(1024)  # 1KB of memory
        self.registers = [0] * 32
        self.pc = 0
        self.cycle = 0

        # Initialize pipeline registers
        self.IF_ID = PipelinedRegister()
        self.ID_EX = PipelinedRegister()
        self.EX_MEM = PipelinedRegister()
        self.MEM_WB = PipelinedRegister()

    def load_program(self, program):
        self.pc = 0
        for i, instruction in enumerate(program):
            self.memory[i * 4:(i + 1) * 4] = instruction.to_bytes(4, byteorder='little')

    def run(self):
        output = ""
        while self.pc < len(self.memory) or self.is_pipeline_active():
            output += self.step()
        return output

    def is_pipeline_active(self):
        return self.IF_ID.valid or self.ID_EX.valid or self.EX_MEM.valid or self.MEM_WB.valid

    def step(self):
        self.cycle += 1

        self.WB_stage()
        self.MEM_stage()
        self.EX_stage()
        self.ID_stage()
        self.IF_stage()
        
        # Return the state of the pipeline for debugging
        return (
            f"Cycle: {self.cycle}\n"
            f"IF/ID: {self.IF_ID.instruction:08X}\n"
            f"ID/EX: {self.ID_EX.instruction:08X}\n"
            f"EX/MEM: {self.EX_MEM.instruction:08X}\n"
            f"MEM/WB: {self.MEM_WB.instruction:08X}\n"
        )


    def IF_stage(self):
        if self.pc < len(self.memory):
            self.IF_ID.instruction = int.from_bytes(self.memory[self.pc:self.pc+4], 'little')
            self.IF_ID.pc = self.pc
            self.IF_ID.valid = True
            self.pc += 4

    def ID_stage(self):
            instruction = self.IF_ID.instruction
            self.ID_EX.instruction = instruction
            self.ID_EX.pc = self.IF_ID.pc

            opcode = instruction & 0x7F
            rd = (instruction >> 7) & 0x1F
            funct3 = (instruction >> 12) & 0x7
            rs1 = (instruction >> 15) & 0x1F
            rs2 = (instruction >> 20) & 0x1F
            funct7 = (instruction >> 25) & 0x7F
            imm = 0

            if opcode == 0x03:  # lw
                imm = instruction >> 20
            elif opcode == 0x23:  # sw
                imm = ((instruction >> 25) << 5) | ((instruction >> 7) & 0x1F)

            self.ID_EX.opcode = opcode
            self.ID_EX.rd = rd
            self.ID_EX.rs1 = rs1
            self.ID_EX.rs2 = rs2
            self.ID_EX.funct3 = funct3
            self.ID_EX.funct7 = funct7
            self.ID_EX.imm = imm
            self.ID_EX.valid = True
            self.IF_ID.valid = False

    def EX_stage(self):
            instruction = self.ID_EX.instruction
            self.EX_MEM.instruction = instruction
            if self.ID_EX.opcode == 0x03:  # lw
                self.EX_MEM.alu_result = self.registers[self.ID_EX.rs1] + self.ID_EX.imm
            elif self.ID_EX.opcode == 0x23:  # sw
                self.EX_MEM.alu_result = self.registers[self.ID_EX.rs1] + self.ID_EX.imm
            elif self.ID_EX.opcode == 0x33:  # R-type (add, sub, mul)
                if self.ID_EX.funct3 == 0x0:
                    if self.ID_EX.funct7 == 0x00:  # add
                        self.EX_MEM.alu_result = self.registers[self.ID_EX.rs1] + self.registers[self.ID_EX.rs2]
                    elif self.ID_EX.funct7 == 0x20:  # sub
                        self.EX_MEM.alu_result = self.registers[self.ID_EX.rs1] - self.registers[self.ID_EX.rs2]
                    elif self.ID_EX.funct7 == 0x01:  # mul
                        self.EX_MEM.alu_result = self.registers[self.ID_EX.rs1] * self.registers[self.ID_EX.rs2]

            self.EX_MEM.rd = self.ID_EX.rd
            self.EX_MEM.rs2 = self.ID_EX.rs2
            self.EX_MEM.opcode = self.ID_EX.opcode
            self.EX_MEM.valid = True
            self.ID_EX.valid = False

    def MEM_stage(self):
            instruction = self.EX_MEM.instruction
            self.MEM_WB.instruction = instruction
            if self.EX_MEM.opcode == 0x03:  # lw
                address = self.EX_MEM.alu_result
                self.MEM_WB.alu_result = int.from_bytes(self.memory[address:address+4], 'little')
            elif self.EX_MEM.opcode == 0x23:  # sw
                address = self.EX_MEM.alu_result
                self.memory[address:address+4] = self.registers[self.EX_MEM.rs2].to_bytes(4, 'little')
            else:
                self.MEM_WB.alu_result = self.EX_MEM.alu_result

            self.MEM_WB.rd = self.EX_MEM.rd
            self.MEM_WB.opcode = self.EX_MEM.opcode
            self.MEM_WB.valid = True
            self.EX_MEM.valid = False

    def WB_stage(self):
            if self.MEM_WB.opcode == 0x03:  # lw
                self.registers[self.MEM_WB.rd] = self.MEM_WB.alu_result
            elif self.MEM_WB.opcode == 0x33:  # R-type (add, sub, mul)
                self.registers[self.MEM_WB.rd] = self.MEM_WB.alu_result
            self.MEM_WB.valid = False


    def ID_stage(self):
            instruction = self.IF_ID.instruction
            self.ID_EX.instruction = instruction
            self.ID_EX.pc = self.IF_ID.pc

            opcode = instruction & 0x7F
            rd = (instruction >> 7) & 0x1F
            funct3 = (instruction >> 12) & 0x7
            rs1 = (instruction >> 15) & 0x1F
            rs2 = (instruction >> 20) & 0x1F
            funct7 = (instruction >> 25) & 0x7F
            imm = 0

            if opcode == 0x03:  # lw
                imm = instruction >> 20
            elif opcode == 0x23:  # sw
                imm = ((instruction >> 25) << 5) | ((instruction >> 7) & 0x1F)

            self.ID_EX.opcode = opcode
            self.ID_EX.rd = rd
            self.ID_EX.rs1 = rs1
            self.ID_EX.rs2 = rs2
            self.ID_EX.funct3 = funct3
            self.ID_EX.funct7 = funct7
            self.ID_EX.imm = imm
            self.ID_EX.valid = True
            self.IF_ID.valid = False
