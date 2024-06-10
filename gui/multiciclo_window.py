import tkinter as tk
from tkinter import ttk
from processor.multiciclo import Multiciclo
import time

class MulticicloWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Multicycle Simulator")
        self.create_widgets()
        self.simulator = Multiciclo()
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

        example_program = [
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
        self.simulator.load_program(example_program)

    def run_program(self):
        print("RUN")

    def run_timed_program(self):
        print("RUN")

    def step_timed(self):
        print("STEP TIME")    

    def step_program(self):
        print("STEP")

    def update_ui(self):
        print("UPDATE UI")

    def update_registers(self):
        print("UPDATE UI")

    def update_memory(self):
        print("UPDATE MEM")