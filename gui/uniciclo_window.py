import tkinter as tk
from processor.uniciclo import Uniciclo
import time

class UnicicloWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Uniciclo Simulator")
        self.create_widgets()
        self.uniciclo = Uniciclo()
        self.start_time = None
        self.execution_time = 0

    def create_widgets(self):
        self.load_button = tk.Button(self.master, text="Load Program", command=self.load_program)
        self.load_button.pack()

        self.run_button = tk.Button(self.master, text="Run Program", command=self.run_program)
        self.run_button.pack()

        self.step_button = tk.Button(self.master, text="Step", command=self.step_program)
        self.step_button.pack()

        self.cycle_label = tk.Label(self.master, text="Cycle: 0")
        self.cycle_label.pack()

        self.time_label = tk.Label(self.master, text="Execution Time: 0.0s")
        self.time_label.pack()

        self.pc_label = tk.Label(self.master, text="PC: 0x00000000")
        self.pc_label.pack()

        self.registers_text = tk.Text(self.master, height=10, width=50)
        self.registers_text.pack()

        self.memory_text = tk.Text(self.master, height=10, width=50)
        self.memory_text.pack()

        self.output_text = tk.Text(self.master, height=10, width=80)
        self.output_text.pack()

    def load_program(self):
        program = [
            0x00000093,  # ADDI x1, x0, 0  -> x1 = 0
            0x00100113,  # ADDI x2, x0, 1  -> x2 = 1
            0x002081B3,  # ADD x3, x1, x2  -> x3 = x1 + x2 = 1
            0x00420223,  # SW x4, 0(x4)    -> Mem[x4] = x4 (store x4 at address in x4)
            0x00318063,  # BEQ x3, x3, 0   -> if x3 == x3, PC = PC + 4 (no-op)
            0xFFF10113,  # ADDI x2, x2, -1 -> x2 = x2 - 1
            0x00200193,  # ADDI x3, x0, 2  -> x3 = 2
        ]
        self.uniciclo.load_program(program)
        self.output_text.insert(tk.END, "Program loaded.\n")

    def run_program(self):
        if self.start_time is None:
            self.start_time = time.time()
        output = self.uniciclo.run()
        self.execution_time = time.time() - self.start_time
        self.update_ui()
        self.output_text.insert(tk.END, output)

    def step_program(self):
        if self.start_time is None:
            self.start_time = time.time()
        output = self.uniciclo.step()
        self.execution_time = time.time() - self.start_time
        self.update_ui()
        self.output_text.insert(tk.END, output)

    def update_ui(self):
        self.cycle_label.config(text=f"Cycle: {self.uniciclo.cycle}")
        self.time_label.config(text=f"Execution Time: {self.execution_time:.2f}s")
        self.pc_label.config(text=f"PC: 0x{self.uniciclo.pc:08X}")
        self.update_registers()
        self.update_memory()

    def update_registers(self):
        self.registers_text.delete('1.0', tk.END)
        for i in range(32):
            self.registers_text.insert(tk.END, f"x{i:02}: 0x{self.uniciclo.registers[i]:08X}\n")

    def update_memory(self):
        self.memory_text.delete('1.0', tk.END)
        for address in range(0, len(self.uniciclo.memory), 4):
            value = int.from_bytes(self.uniciclo.memory[address:address+4], byteorder='little')
            self.memory_text.insert(tk.END, f"0x{address:08X}: 0x{value:08X}\n")
