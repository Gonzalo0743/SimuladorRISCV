class Assembler:
    def __init__(self):
        self.opcodes = {
            'lw': 0x03,
            'sw': 0x23,
            'add': 0x33,
            'sub': 0x33,
            'mul': 0x33
        }
        self.funct3 = {
            'lw': 0x2,
            'sw': 0x2,
            'add': 0x0,
            'sub': 0x0,
            'mul': 0x0
        }
        self.funct7 = {
            'add': 0x00,
            'sub': 0x20,
            'mul': 0x01
        }

    def parse_register(self, reg_str):
        if reg_str[0] != 'x':
            raise ValueError(f"Invalid register format: {reg_str}")
        return int(reg_str[1:])

    def assemble(self, code):
        lines = code.strip().split('\n')
        program = []
        for line in lines:
            parts = line.replace(',', '').split()
            inst = parts[0]
            if inst in ['lw', 'sw']:
                rd = self.parse_register(parts[1])
                offset, rs1 = parts[2].split('(')
                rs1 = self.parse_register(rs1[:-1])
                offset = int(offset)
                instruction = (offset << 20) | (rs1 << 15) | (self.funct3[inst] << 12) | (rd << 7) | self.opcodes[inst]
            elif inst in ['add', 'sub', 'mul']:
                rd = self.parse_register(parts[1])
                rs1 = self.parse_register(parts[2])
                rs2 = self.parse_register(parts[3])
                instruction = (self.funct7[inst] << 25) | (rs2 << 20) | (rs1 << 15) | (self.funct3[inst] << 12) | (rd << 7) | self.opcodes[inst]
            else:
                raise ValueError(f"Unknown instruction: {inst}")
            program.append(instruction)
        return program
