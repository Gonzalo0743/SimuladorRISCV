class Multiciclo:
    def __init__(self):
        self.registers = [0] * 32  # Registros
        self.memory = [0] * 1024   # Memoria

        self.pc = 0                # Program counter
        self.current_instruction = None
        self.decoded_instruction = None
        self.address = None
        self.result = None
        self.cycle_count = 0       
        self.instruction_count = 0 
        
        # FSM States
        self.states = ['fetch', 'decode', 'memory_address', 'memory_read', 'memory_write_back', 'execute', 'write_back']
        self.current_state = 'fetch'

    def load_program(self, program):  #Carga programa en memoria
        self.memory[:len(program)] = program

    def fetch(self): #Funcion para etapa de fetch
        self.current_instruction = self.memory[self.pc]
        self.pc += 1
        self.current_state = 'decode'
        self.cycle_count += 1

    def decode(self): #Funcion para etapa decode
        instruction = self.current_instruction
        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x07
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F
        imm = self.sign_extend((instruction >> 20) & 0xFFF, 12)
        self.decoded_instruction = (opcode, rd, funct3, rs1, rs2, funct7, imm)
        self.current_state = 'memory_address'
        self.cycle_count += 1

    def memory_address(self): #Funcion para memaddr
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode in [0x03, 0x23]:  # Load/Store instructions
            self.address = self.registers[rs1] + imm
        else:
            self.address = None  # No address needed for non-memory instructions
        self.current_state = 'memory_read'
        self.cycle_count += 1

    def memory_read(self): #Funcion para memard
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode == 0x03:  # Load
            self.result = self.memory[self.address]
        self.current_state = 'memory_write_back'
        self.cycle_count += 1

    def memory_write_back(self): #Funcion para mem wb
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode == 0x23:  # Store
            self.memory[self.address] = self.registers[rs2]
        self.current_state = 'execute'
        self.cycle_count += 1

    def execute(self): #Funcion para xecute
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode == 0x33:  # Tipo R
            if funct3 == 0x0:
                if funct7 == 0x00:
                    self.result = self.registers[rs1] + self.registers[rs2]  # add
                elif funct7 == 0x20:
                    self.result = self.registers[rs1] - self.registers[rs2]  # sub
            elif funct3 == 0x7:
                self.result = self.registers[rs1] & self.registers[rs2]  # and
            elif funct3 == 0x6:
                self.result = self.registers[rs1] | self.registers[rs2]  # or
            elif funct3 == 0x4:
                self.result = self.registers[rs1] ^ self.registers[rs2]  # xor
        elif opcode == 0x03:  
            self.address = self.registers[rs1] + imm
        elif opcode == 0x13:  # Tipo y
            if funct3 == 0x0:
                self.result = self.registers[rs1] + imm  # addi
            elif funct3 == 0x7:
                self.result = self.registers[rs1] & imm  # andi
            elif funct3 == 0x6:
                self.result = self.registers[rs1] | imm  # ori
            elif funct3 == 0x4:
                self.result = self.registers[rs1] ^ imm  # xori
        elif opcode == 0x23: 
            self.address = self.registers[rs1] + imm
        elif opcode == 0x23:  
            self.address = self.registers[rs1] + imm #fix
        elif opcode == 0x63: 
            if funct3 == 0x0 and self.registers[rs1] == self.registers[rs2]:  # beq
                self.pc += imm
            elif funct3 == 0x1 and self.registers[rs1] != self.registers[rs2]:  # bne
                self.pc += imm
        self.current_state = 'write_back'
        self.cycle_count += 1

    def write_back(self):
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode in [0x33, 0x03, 0x13]: 
            self.registers[rd] = self.result
        self.current_state = 'fetch'
        self.cycle_count += 1
        self.instruction_count += 1  #Incrementa contador de instrucciones

    def run(self):
        while True:
            if self.current_state == 'fetch':
                self.fetch()
            elif self.current_state == 'decode':
                self.decode()
            elif self.current_state == 'memory_address':
                self.memory_address()
            elif self.current_state == 'memory_read':
                self.memory_read()
            elif self.current_state == 'memory_write_back':
                self.memory_write_back()
            elif self.current_state == 'execute':
                self.execute()
            elif self.current_state == 'write_back':
                self.write_back()
            if self.pc >= len(self.memory) or self.current_instruction == 0:  #Condicion para terminar programa
                break 

        # Calculadora de CPI
        if self.instruction_count > 0:
            cpi = self.cycle_count / self.instruction_count
            print(f"CPI: {cpi:.2f}")
        else:
            print("No instructions executed.")

    def sign_extend(self, value, bits):
        sign_bit = 1 << (bits - 1)
        return (value & (sign_bit - 1)) - (value & sign_bit)

#test
processor = Multiciclo()
code = [
            0x00200093,  # addi x1, x0, 2
            0x00300113,  # addi x2, x0, 3
            0x002081b3,  # add x3, x1, x2
            0x0000a023,  # sw x0, 0(x1)
            0x00112083,  # lw x1, 1(x2)
            0x00006133,  # and x2, x1, x0
            0x000041B3,  # or x3, x0, x1
            0x00400063,  # beq x0, x0, 4 (salto si igual)
            0x00500063   # bne x0, x0, 5 (salto si no igual)
        ]
processor.load_program(code)
processor.run()

print(processor.registers)




