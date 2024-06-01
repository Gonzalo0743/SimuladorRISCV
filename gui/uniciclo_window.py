import tkinter as tk
from tkinter import ttk
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
        # Create a main frame
        self.main_frame = tk.Frame(self.master, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Add control buttons at the top
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack(fill=tk.X, pady=5)

        self.load_button = tk.Button(self.controls_frame, text="Load Program", command=self.load_program)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.run_button = tk.Button(self.controls_frame, text="Run Program", command=self.run_program)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.step_button = tk.Button(self.controls_frame, text="Step", command=self.step_program)
        self.step_button.pack(side=tk.LEFT, padx=5)

        self.run_timed_button = tk.Button(self.controls_frame, text="Run Timed", command=self.run_timed_program)
        self.run_timed_button.pack(side=tk.LEFT, padx=5)

        # Add status labels
        self.status_frame = tk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=5)

        self.cycle_label = tk.Label(self.status_frame, text="Cycle: 0")
        self.cycle_label.pack(side=tk.LEFT, padx=5)

        self.time_label = tk.Label(self.status_frame, text="Execution Time: 0.0s")
        self.time_label.pack(side=tk.LEFT, padx=5)

        self.pc_label = tk.Label(self.status_frame, text="PC: 0x00000000")
        self.pc_label.pack(side=tk.LEFT, padx=5)

        # Add a separator
        separator = tk.Frame(self.main_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, pady=10)

        # Create text areas for registers and memory with labels
        self.data_frame = tk.Frame(self.main_frame)
        self.data_frame.pack(fill=tk.BOTH, expand=True)

        self.registers_label = tk.Label(self.data_frame, text="Registers", font=("Helvetica", 14))
        self.registers_label.grid(row=0, column=0, padx=10, pady=5)

        self.registers_text = tk.Text(self.data_frame, height=10, width=30)
        self.registers_text.grid(row=1, column=0, padx=10, pady=5)

        self.memory_label = tk.Label(self.data_frame, text="Memory", font=("Helvetica", 14))
        self.memory_label.grid(row=0, column=1, padx=10, pady=5)

        self.memory_text = tk.Text(self.data_frame, height=10, width=30)
        self.memory_text.grid(row=1, column=1, padx=10, pady=5)

        # Add output text area with a label
        self.output_label = tk.Label(self.data_frame, text="Output", font=("Helvetica", 14))
        self.output_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.output_text = tk.Text(self.data_frame, height=10, width=80)
        self.output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

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

    def run_timed_program(self):
        if self.start_time is None:
            self.start_time = time.time()
        self.master.after(1000, self.step_timed)

    def step_timed(self):
        output = self.uniciclo.step()
        self.execution_time = time.time() - self.start_time
        self.update_ui()
        self.output_text.insert(tk.END, output)
        if self.uniciclo.pc < len(self.uniciclo.memory):
            self.master.after(1000, self.step_timed)

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
