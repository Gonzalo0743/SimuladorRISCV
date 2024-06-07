class Multiciclo:
    def __init__(self):
        self.registers = [0] * 32  # Resgistros
        self.memory = [0] * 1024   # Memoria
        self.pc = 0                # Program counter
        self.current_instruction = None
        self.current_stage = 'fetch'
        self.decoded_instruction = None
        self.address = None
        self.result = None

    def load_program(self, program): #Carga programa en memoria
        self.memory[:len(program)] = program

    def fetch(self):
        self.current_instruction = self.memory[self.pc]
        self.pc += 1
        self.current_stage = 'decode'

    def decode(self):
        instruction = self.current_instruction
        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x07
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F
        imm = self.sign_extend((instruction >> 20) & 0xFFF, 12)
        self.decoded_instruction = (opcode, rd, funct3, rs1, rs2, funct7, imm)
        self.current_stage = 'memory_address'

    def memory_address(self):
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode in [0x03, 0x23]:  # Instrucciones Load/Store 
            self.address = self.registers[rs1] + imm
        else:
            self.address = None  
        self.current_stage = 'memory_read'

    def memory_read(self):
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode == 0x03:  # Load
            self.result = self.memory[self.address]
        else:
            self.result = self.address  # Pass the address as result for other instructions
        self.current_stage = 'memory_write_back'

    def memory_write_back(self):
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode == 0x23:  # Store
            self.memory[self.address] = self.registers[rs2]
        self.current_stage = 'execute'

    def execute(self):
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode == 0x33:  # R-type
            if funct3 == 0x0 and funct7 == 0x00:
                self.result = self.registers[rs1] + self.registers[rs2] #add
            elif funct3 == 0x0 and funct7 == 0x20:
                self.result = self.registers[rs1] - self.registers[rs2] #sub
        elif opcode == 0x13:  # I-type
            self.result = self.registers[rs1] + imm #addi
        self.current_stage = 'write_back'

    def write_back(self):
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode in [0x33, 0x03, 0x13]:  # R-type, Load, I-type
            self.registers[rd] = self.result
        self.current_stage = 'fetch'

    def run(self, cycles):
        for _ in range(cycles):
            if self.current_stage == 'fetch':
                self.fetch()
            elif self.current_stage == 'decode':
                self.decode()
            elif self.current_stage == 'memory_address':
                self.memory_address()
            elif self.current_stage == 'memory_read':
                self.memory_read()
            elif self.current_stage == 'memory_write_back':
                self.memory_write_back()
            elif self.current_stage == 'execute':
                self.execute()
            elif self.current_stage == 'write_back':
                self.write_back()

    def sign_extend(self, value, bits):
        sign_bit = 1 << (bits - 1)
        return (value & (sign_bit - 1)) - (value & sign_bit)


#Prueba
processor = Multiciclo()
instructions = [
    0x00200093,  # addi x1, x0, 2
    0x00300113,  # addi x2, x0, 3
    0x002081B3,  # add x3, x1, x2
]
processor.load_program(instructions)
processor.run(25)

print(processor.registers)




