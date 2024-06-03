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
        matrix_a = [1, 2, 3, 4]
        matrix_b = [5, 6, 7, 8]
        self.uniciclo.load_program(program)
        self.uniciclo.load_matrices(matrix_a, matrix_b)
        self.output_text.insert(tk.END, "Matrix multiplication program loaded.\n")


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
