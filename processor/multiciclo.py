class Multiciclo:
    def __init__(self):
        self.registers = [0] * 32  # Registros
        self.memory = bytearray(1024)  # Memoria as bytearray

        self.pc = 0                # Program counter
        self.current_instruction = None
        self.decoded_instruction = None
        self.address = None
        self.result = None
        self.cycle_count = 0       
        self.instruction_count = 0 
        self.running = True  
        
        # Estados FSM
        self.states = ['fetch', 'decode', 'memory_access', 'memory_write_back', 'execute', 'write_back']
        self.current_state = 'fetch'


    def load_program(self, program):  # Carga programa en memoria
        self.pc = 0
        for i, instruction in enumerate(program):
            self.memory[i * 4:(i + 1) * 4] = instruction.to_bytes(4, byteorder='little')

    def fetch(self):  # Funcion para etapa de fetch
        self.current_instruction = int.from_bytes(self.memory[self.pc:self.pc + 4], 'little')
        self.pc += 4
        self.current_state = 'decode'
        self.cycle_count += 1

    def decode(self):  # Funcion para etapa decode
        instruction = self.current_instruction
        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x07
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F
        imm = self.sign_extend((instruction >> 20) & 0xFFF, 12)
        self.decoded_instruction = (opcode, rd, funct3, rs1, rs2, funct7, imm)
        self.current_state = 'memory_access'
        self.cycle_count += 1

    def memory_access(self):  # Funcion combinada para memaddr y memread
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode == 0x03:  # Load
            self.address = self.registers[rs1] + imm
            self.result = int.from_bytes(self.memory[self.address:self.address + 4], 'little')
        elif opcode == 0x23:  # Store
            self.address = self.registers[rs1] + imm
        else:
            self.address = None  # No address needed for non-memory instructions
        self.current_state = 'memory_write_back' if opcode == 0x23 else 'execute'
        self.cycle_count += 1

    def memory_write_back(self):  # Funcion para mem wb
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode == 0x23:  # Store
            self.memory[self.address:self.address + 4] = self.registers[rs2].to_bytes(4, 'little')
        self.current_state = 'execute'
        self.cycle_count += 1

    def execute(self):  # Funcion para xecute
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode == 0x33:  # Tipo R
            if funct3 == 0x0:
                if funct7 == 0x00:
                    self.result = self.registers[rs1] + self.registers[rs2]  # add
                elif funct7 == 0x20:
                    self.result = self.registers[rs1] - self.registers[rs2]  # sub
                elif funct7 == 0x01:
                    self.result = self.registers[rs1] * self.registers[rs2]  # mul
            elif funct3 == 0x7:
                self.result = self.registers[rs1] & self.registers[rs2]  # and
            elif funct3 == 0x6:
                self.result = self.registers[rs1] | self.registers[rs2]  # or
            elif funct3 == 0x4:
                self.result = self.registers[rs1] ^ self.registers[rs2]  # xor
        elif opcode == 0x03:  
            self.address = self.registers[rs1] + imm
        elif opcode == 0x13:  # Tipo I
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
        self.instruction_count += 1  # Incrementa contador de instrucciones

    def step(self):
        state_actions = {
            'fetch': self.fetch,
            'decode': self.decode,
            'memory_access': self.memory_access,
            'memory_write_back': self.memory_write_back,
            'execute': self.execute,
            'write_back': self.write_back
        }
        if self.current_state in state_actions:
            state_actions[self.current_state]()
        cpi = self.CPI_counter()
        instruction = self.current_instruction
        output = f"PC: 0x{self.pc - 4:08X}, Cycle: {self.cycle_count}, Instruction: 0x{instruction:08X}, CPI: {cpi:.2f}\n"
        return output

    def run(self):
        output = ""
        while self.running:
            output += self.step()
            if self.pc >= len(self.memory) or self.current_instruction == 0:  # Condicion para terminar programa
                self.running = False

        return output
    
    # Calculadora de CPI
    def CPI_counter(self):
        if self.instruction_count > 0:
            cpi = self.cycle_count / self.instruction_count
            return cpi
        else:
            return 1
        
    def sign_extend(self, value, bits):
        sign_bit = 1 << (bits - 1)
        return (value & (sign_bit - 1)) - (value & sign_bit)


# Test
processor = Multiciclo()
code = [
    0x00200093,  # addi x1, x0, 2
    0x00300113,  # addi x2, x0, 3
    0x002081b3   # add x3, x1, x2
]
processor.load_program(code)
processor.run()

print(processor.registers)
