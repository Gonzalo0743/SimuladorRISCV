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
        self.memory_data = 0
        self.stage = ""


'''
    Control de riesgos:
        F: Comprueba  hazard de datos si una instruccion lw va a intentar leer la direccion de memoria que otra instruccion sw está escribiendo
        ID: Comprueba si alguna instruccion dependiente intenta leer algún registro que esté siendo escrito por otra instrucción dependiente o lw 
'''

class Segmentado_Stalls:
    def __init__(self):
        self.memory = bytearray(1024)  # 1KB of memory
        self.registers = [0] * 32
        self.pc = 0
        self.cycle = 0
        self.instruction_counter = 0
        self.counter = 0

        # Initialize pipeline registers
        self.IF_ID = PipelinedRegister()
        self.ID_EX = PipelinedRegister()
        self.EX_MEM = PipelinedRegister()
        self.MEM_WB = PipelinedRegister()
        self.WB = PipelinedRegister()  # Explicit WB stage

        # Hazard detection
        self.stall = False
        self.flush = False  # Flag to indicate flushing after a stall


    def load_program(self, program):
        self.pc = 0
        for i, instruction in enumerate(program):
            self.memory[i * 4:(i + 1) * 4] = instruction.to_bytes(4, byteorder='little')

    def run(self):
        output = ""
        while self.is_pipeline_active() == True:
            output += self.step()
        return output

    def is_pipeline_active(self):
        if self.IF_ID.valid == True or self.ID_EX.valid == True or self.EX_MEM.valid == True or self.MEM_WB.valid == True or self.WB.valid == True:
            return True
        else:
            return False
    
    #Calculadora CPI
    def CPI_counter(self):
        if self.instruction_counter > 0:
            cpi = self.cycle / self.instruction_counter
            return cpi
        else:
            return 1
    
    def check_stall(self):
        if self.ID_EX.instruction != 00000000 and self.EX_MEM.instruction != 00000000:
                if (self.ID_EX.instruction == self.EX_MEM.instruction):
                    self.EX_MEM.instruction = 0
                    print ("STALL en ID")

        elif self.EX_MEM.instruction != 00000000 and self.MEM_WB.instruction != 00000000:
                if (self.EX_MEM.instruction == self.MEM_WB.instruction):
                    self.EX_MEM.instruction = 0
                    print ("STALL en EX")

        elif self.MEM_WB.instruction != 00000000 and self.WB.instruction != 00000000:
                if (self.MEM_WB.instruction == self.WB.instruction):
                    self.MEM_WB.instruction = 0
                    print ("STALL en MEM")


        else:
            return (
                f"Cycle: {self.cycle}\n"
                f"{self.IF_ID.instruction:08X} ({self.IF_ID.stage})\n"
                f"{self.ID_EX.instruction:08X} ({self.ID_EX.stage})\n"
                f"{self.EX_MEM.instruction:08X} ({self.EX_MEM.stage})\n"
                f"{self.MEM_WB.instruction:08X} ({self.MEM_WB.stage})\n"
                f"{self.WB.instruction:08X} ({self.WB.stage})\n"
            )



    def step(self):
        self.cycle += 1

        # Execute stages based on stall condition
        if self.stall == False:
            self.WB_stage()
            self.MEM_stage()
            self.EX_stage()
            self.ID_stage()
            self.IF_stage()
        else:
            self.WB_stage()
            self.MEM_stage()
            self.EX_stage()
            if self.counter == 1:
                self.stall = False
            else:
                self.counter -=1
        
        cpi = self.CPI_counter()
        self.check_stall()

        if self.IF_ID.instruction == 0 and self.ID_EX.instruction == 0 and self.EX_MEM.instruction == 0 and self.MEM_WB.instruction == 0 and self.WB.instruction == 0:
            self.IF_ID.valid = False
            self.ID_EX.valid = False
            self.EX_MEM.valid = False
            self.MEM_WB.valid = False
            self.WB.valid = False


        if self.stall == False:
            return (
                    f"Cycle: {self.cycle}\n"
                    f"{self.IF_ID.instruction:08X} ({self.IF_ID.stage})\n"
                    f"{self.ID_EX.instruction:08X} ({self.ID_EX.stage})\n"
                    f"{self.EX_MEM.instruction:08X} ({self.EX_MEM.stage})\n"
                    f"{self.MEM_WB.instruction:08X} ({self.MEM_WB.stage})\n"
                    f"{self.WB.instruction:08X} ({self.WB.stage})\n"
                )
        else:
            return (
                    f"Cycle: {self.cycle}\n"
                    f"{self.IF_ID.instruction:08X} ({self.IF_ID.stage})\n"
                    f"{self.ID_EX.instruction:08X} ({self.ID_EX.stage})\n"
                    f"{self.EX_MEM.instruction:08X} ({self.EX_MEM.stage})\n"
                    f"{self.MEM_WB.instruction:08X} ({self.MEM_WB.stage})\n"
                    f"{self.WB.instruction:08X} ({self.WB.stage})\n"
                    f"Detección de hazard. STALL insertado\n"
                )

    def IF_stage(self):
        if self.pc < len(self.memory):
            self.IF_ID.instruction = int.from_bytes(self.memory[self.pc:self.pc+4], 'little')
            self.IF_ID.pc = self.pc
            self.IF_ID.stage = "IF"
            self.pc += 4
            
            # Deteccion de data hazard, lw en FETCH y sw en WB
            #               si lw en F                          si sw en WB
            if (self.IF_ID.instruction & 0x7F) == 0x03 and (self.WB.instruction & 0x7F) == 0x23:
                if self.IF_ID.rs1 == self.WB.rd:
                    self.IF_ID.valid = False
                    self.pc -= 4
                    print (f"Hazard entre lw y sw.  Ciclo: {self.cycle}\n")
            else:
                self.IF_ID.valid = True
           

    def ID_stage(self):
        if self.IF_ID.valid:
            instruction = self.IF_ID.instruction

            # Proceed with normal instruction decoding
            self.ID_EX.instruction = instruction
            self.ID_EX.pc = self.IF_ID.pc
            self.ID_EX.stage = "ID"

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

            # Control de riesgos
            #  add y mul acceden a sus operandos en esta etapa, puede haber hazard de datos por acceder 
            if self.ID_EX.instruction != 0 and self.MEM_WB.instruction != 0:
                if self.ID_EX.opcode == 0x33:
                    # no hace falta para sw
                    if (self.EX_MEM.instruction & 0x7F) == 0x23 or (self.WB.instruction & 0x7F) == 0x23:
                        self.ID_EX.valid = True
                    if self.ID_EX.rs1 == self.EX_MEM.rd or self.ID_EX.rs2 == self.EX_MEM.rd:
                        self.stall = True
                        self.counter += 1
                        print (f"Hazard en DECODE 1.  Ciclo: {self.cycle}\n")
                    if self.ID_EX.rs1 == self.MEM_WB.rd or self.ID_EX.rs2 == self.MEM_WB.rd:
                        self.pc -= 4
                        self.counter += 2
                        self.stall = True
                        print (f"Hazard en DECODE 2.  Ciclo: {self.cycle}\n")
                    else:
                        self.ID_EX.valid = True
            else:
                self.ID_EX.valid = True

        
            


    def EX_stage(self):
        if self.ID_EX.valid:

            instruction = self.ID_EX.instruction
            self.EX_MEM.instruction = instruction
            self.EX_MEM.stage = "EX"

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
        if self.EX_MEM.valid:
            instruction = self.EX_MEM.instruction
            self.MEM_WB.instruction = instruction
            self.MEM_WB.stage = "MEM"

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
        if self.MEM_WB.valid:
            if self.WB.instruction != 0:
                self.instruction_counter += 1
            self.WB.instruction = self.MEM_WB.instruction
            self.WB.stage = "WB"

            if self.MEM_WB.opcode == 0x03:  # lw
                self.registers[self.MEM_WB.rd] = self.MEM_WB.alu_result
            elif self.MEM_WB.opcode == 0x33:  # R-type (add, sub, mul)
                self.registers[self.MEM_WB.rd] = self.MEM_WB.alu_result

            self.WB.valid = True
            self.MEM_WB.valid = False

