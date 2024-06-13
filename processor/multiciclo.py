class Multiciclo:
    def __init__(self):
        self.registers = [0] * 32  # Registros
        self.memory = bytearray(1024)  #Memoria

        #Variables
        self.pc = 0  # Program counter
        self.current_instruction = None
        self.decoded_instruction = None
        self.address = None
        self.result = None
        self.cycle_count = 0
        self.instruction_count = 0
        self.running = True

        # Estados FSM 
        self.states = ['fetch', 'decode', 'memory_access', 'execute', 'write_back']
        self.current_state = 'fetch'

      #Carga programa en memoria
    def load_program(self, program):
        self.pc = 0
        for i, instruction in enumerate(program):
            self.memory[i * 4:(i + 1) * 4] = instruction.to_bytes(4, byteorder='little')
    # Etapa fetch
    def fetch(self):  # Etapa fetch
        self.current_instruction = int.from_bytes(self.memory[self.pc:self.pc + 4], 'little')
        self.pc += 4
        self.current_state = 'decode'
        self.cycle_count += 1
    # Decodificador
    def decode(self):  # Decodificador
        instruction = self.current_instruction
        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x07
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F
        imm = self.sign_extend((instruction >> 20) & 0xFFF, 12)
        self.decoded_instruction = (opcode, rd, funct3, rs1, rs2, funct7, imm)

        # Determina el siguiente estado
        if opcode == 0x73 and funct3 == 0x0:  #Verifica que le programa siga, si no, ebreak
            self.running = False
            self.current_state = 'fetch'
            self.cycle_count += 1
            return f"EBREAK encountered. Halting execution.\n"

        elif opcode in [0x03, 0x23]:  
            self.current_state = 'memory_access'
        elif opcode == 0x33 or opcode == 0x13:  
            self.current_state = 'execute'
        else: 
            self.current_state = 'write_back'
        self.cycle_count += 1

    # Acceso a memoria
    def memory_access(self):  
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode == 0x03:  #lw
            self.address = self.registers[rs1] + imm
            self.result = int.from_bytes(self.memory[self.address:self.address + 4], 'little')
            self.current_state = 'write_back'
        elif opcode == 0x23:  #sw
            self.address = self.registers[rs1] + imm
            self.memory[self.address:self.address + 4] = self.registers[rs2].to_bytes(4, 'little')
            self.current_state = 'write_back'
        
        self.cycle_count += 1
    #Ejecuta instrucciones tipo R
    def execute(self):  # Execute stage
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode == 0x33:  # R-type
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
        elif opcode == 0x13:  # I-type
            if funct3 == 0x0:
                self.result = self.registers[rs1] + imm  # addi
            elif funct3 == 0x7:
                self.result = self.registers[rs1] & imm  # andi
            elif funct3 == 0x6:
                self.result = self.registers[rs1] | imm  # ori
            elif funct3 == 0x4:
                self.result = self.registers[rs1] ^ imm  # xori
        self.current_state = 'write_back'
        self.cycle_count += 1
    #Verifica registros y vuelve a fetch
    def write_back(self):  
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decoded_instruction
        if opcode in [0x33, 0x03, 0x13]:  
            self.registers[rd] = self.result
        self.current_state = 'fetch'
        self.cycle_count += 1
        self.instruction_count += 1  

    #Ejecuta un ciclo
    def step(self): 
        state_actions = {
            'fetch': self.fetch,
            'decode': self.decode,
            'memory_access': self.memory_access,
            'execute': self.execute,
            'write_back': self.write_back
        }
        if self.current_state in state_actions:
            output = state_actions[self.current_state]()
            if output:
                return output
        cpi = self.CPI_counter()
        instruction = self.current_instruction
        output = f"PC: 0x{self.pc - 4:08X}, Cycle: {self.cycle_count}, Instruction: 0x{instruction:08X}, State: {self.current_state}\n"
        return output
    
    #Ejecuta steps hasta terminar
    def run(self):  
        output = ""
        while self.running:
            output += self.step()
            if self.pc >= len(self.memory) or self.current_instruction == 0: 
                self.running = False
        return output

    #Calculadora CPI
    def CPI_counter(self):
        if self.instruction_count > 0:
            cpi = self.cycle_count / self.instruction_count
            return cpi
        else:
            return 1
        
    #Extension de signo
    def sign_extend(self, value, bits):  
        sign_bit = 1 << (bits - 1)
        return (value & (sign_bit - 1)) - (value & sign_bit)
    
processor = Multiciclo()
code = [
    0x00200093,  # addi x1, x0, 2
    0x00300113,  # addi x2, x0, 3
    0x002081B3,  # add x3, x1, x2
    0x00112023,  # sw x1, 0(x2) -> Memory[x2 + 0] = x1
    0x00012103,  # lw x3, 0(x2) -> x3 = Memory[x2 + 0]
    0x00100073   # ebreak
]
processor.load_program(code)
output = processor.run()

print(output)
print(processor.registers)  # Print registers to see the result

