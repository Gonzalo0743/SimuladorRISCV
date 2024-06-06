class multiciclo:
    def __init__(self):
        self.registers = [0] * 32  # Registros
        self.memory = [0] * 1024   # Memoria
        self.pc = 0                


    def load_program(self, code):
        self.memory[:len(code)] = code #Carga el programa a memoria

    def fetch(self):
        print("Add")

    def decode(self):
        print("Add")

    def execute(self):
        print("Add")

    def memory_access(self):
        print("Add")

    def write_back(self):
        print("Add")




