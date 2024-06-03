class Uniciclo:
    def __init__(self):
        self.registers = [0] * 32
        self.memory = bytearray(48)  # Ajustar tamaño de memoria según necesidad
        self.pc = 0
        self.cycle = 0

    def load_program(self, program):
        for i, instr in enumerate(program):
            self.memory[i * 4:i * 4 + 4] = instr.to_bytes(4, byteorder='little')

    def load_matrices(self, matrix_a, matrix_b):
        for i, val in enumerate(matrix_a):
            self.memory[i * 4:i * 4 + 4] = val.to_bytes(4, byteorder='little')
        for i, val in enumerate(matrix_b, 4):
            self.memory[i * 4:i * 4 + 4] = val.to_bytes(4, byteorder='little')

    def run(self):
        output = ""
        while self.pc < len(self.memory):
            output += self.step()
        return output

    def step(self):
        instruction = int.from_bytes(self.memory[self.pc:self.pc + 4], byteorder='little')
        # Decodificar e implementar instrucciones...
        # ...
        self.pc += 4
        self.cycle += 1
        return f"Cycle {self.cycle}: PC = 0x{self.pc:08X}\n"

# Programa de prueba
program = [
    0x00000293,  # lw x5, 0(x0)
    0x00400313,  # lw x6, 4(x0)
    0x00800393,  # lw x7, 8(x0)
    0x00C00413,  # lw x8, 12(x0)
    0x01000493,  # lw x9, 16(x0)
    0x01400513,  # lw x10, 20(x0)
    0x01800593,  # lw x11, 24(x0)
    0x01C00613,  # lw x12, 28(x0)
    0x00A286B3,  # mul x13, x5, x9
    0x00B30733,  # mul x14, x6, x11
    0x00E6E733,  # add x15, x13, x14
    0x020007A3,  # sw x15, 32(x0)
    0x00A287B3,  # mul x15, x5, x10
    0x00B30833,  # mul x16, x6, x12
    0x00F807B3,  # add x15, x15, x16
    0x024007A3,  # sw x15, 36(x0)
    0x00A287B3,  # mul x15, x7, x9
    0x00B30833,  # mul x16, x8, x11
    0x00F807B3,  # add x15, x15, x16
    0x028007A3,  # sw x15, 40(x0)
    0x00A287B3,  # mul x15, x7, x10
    0x00B30833,  # mul x16, x8, x12
    0x00F807B3,  # add x15, x15, x16
    0x02C007A3,  # sw x15, 44(x0)
]

# Matrices de entrada
matrix_a = [1, 2, 3, 4]
matrix_b = [5, 6, 7, 8]

# Instanciar y cargar el programa
uniciclo = Uniciclo()
uniciclo.load_program(program)
uniciclo.load_matrices(matrix_a, matrix_b)

# Ejecutar y ver resultados
output = uniciclo.run()
print(output)

# Verificar resultado en memoria
result = []
for i in range(32, 48, 4):
    result.append(int.from_bytes(uniciclo.memory[i:i + 4], byteorder='little'))
print(f"Matrix C: {result}")
