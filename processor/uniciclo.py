class Uniciclo:
    def __init__(self):
        self.pc = 0
        self.registers = [0] * 32
        self.memory = [0] * 1024
        self.instructions = []

    def load_program(self, program):
        self.instructions = program

    def execute_instruction(self, instruction):
        # Aquí se debe implementar la ejecución de instrucciones RISCV
        pass

    def run(self):
        output = ""
        while self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            self.execute_instruction(instruction)
            self.pc += 1
            output += f"Executed instruction at PC: {self.pc}\n"
        return output
