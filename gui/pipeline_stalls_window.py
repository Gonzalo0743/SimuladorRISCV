import tkinter as tk
from processor.pipeline_stalls import Segmentado_Stalls  # Importa el procesador segmentado en lugar del uniciclo
from processor.assembler import Assembler
import time

class Segmentado_Stalls_Window:
    def __init__(self, master):
        self.master = master
        self.master.title("Segmentado con Stalls Simulator")
        self.create_widgets()
        self.segmentado = Segmentado_Stalls()
        self.assembler = Assembler()
        self.start_time = None
        self.execution_time = 0

    def create_widgets(self):
        self.main_frame = tk.Frame(self.master, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

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

        self.status_frame = tk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=5)

        self.cycle_label = tk.Label(self.status_frame, text="Cycle: 0")
        self.cycle_label.pack(side=tk.LEFT, padx=5)

        self.time_label = tk.Label(self.status_frame, text="Execution Time: 0.0s")
        self.time_label.pack(side=tk.LEFT, padx=5)

        self.pc_label = tk.Label(self.status_frame, text="PC: 0x00000000")
        self.pc_label.pack(side=tk.LEFT, padx=5)

        separator = tk.Frame(self.main_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, pady=10)

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

        self.assembly_label = tk.Label(self.data_frame, text="Assembly Code", font=("Helvetica", 14))
        self.assembly_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.assembly_text = tk.Text(self.data_frame, height=10, width=80)
        self.assembly_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.output_label = tk.Label(self.data_frame, text="Output", font=("Helvetica", 14))
        self.output_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.output_text = tk.Text(self.data_frame, height=10, width=80)
        self.output_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def load_program(self):
        assembly_code = self.assembly_text.get("1.0", tk.END)
        try:
            machine_code = self.assembler.assemble(assembly_code)
            self.segmentado.load_program(machine_code)
            self.output_text.insert(tk.END, "Assembly program loaded.\n")
        except ValueError as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def run_program(self):
        if self.start_time is None:
            self.start_time = time.time()
        while self.segmentado.pc < len(self.segmentado.memory):
            output = self.segmentado.step()
            self.execution_time = time.time() - self.start_time
            self.update_ui()
            self.output_text.insert(tk.END, output)
        self.output_text.insert(tk.END, "Program execution finished.\n")

    def run_timed_program(self):
        if self.start_time is None:
            self.start_time = time.time()
        self.master.after(1000, self.step_timed)

    def step_timed(self):
        if self.segmentado.pc < len(self.segmentado.memory):
            output = self.segmentado.step()
            self.execution_time = time.time() - self.start_time
            self.update_ui()
            self.output_text.insert(tk.END, output)
            self.master.after(1000, self.step_timed)
        else:
            self.output_text.insert(tk.END, "Program execution finished.\n")

    def step_program(self):
        if self.start_time is None:
            self.start_time = time.time()
        if self.segmentado.pc < len(self.segmentado.memory):
            output = self.segmentado.step()
            self.execution_time = time.time() - self.start_time
            self.update_ui()
            self.output_text.insert(tk.END, output)
        else:
            self.output_text.insert(tk.END, "Program execution finished.\n")

    def update_ui(self):
        self.cycle_label.config(text=f"Cycle: {self.segmentado.cycle}")
        self.time_label.config(text=f"Execution Time: {self.execution_time:.2f}s")
        self.pc_label.config(text=f"PC: 0x{self.segmentado.pc:08X}")
        self.update_registers()
        self.update_memory()

    def update_registers(self):
        self.registers_text.delete('1.0', tk.END)
        for i in range(len(self.segmentado.registers)):
            self.registers_text.insert(tk.END, f"x{i}: 0x{self.segmentado.registers[i]:08X}\n")

    def update_memory(self):
        self.memory_text.delete('1.0', tk.END)
        for addr in range(0, len(self.segmentado.memory), 4):
            value = int.from_bytes(self.segmentado.memory[addr:addr+4], 'little')
            self.memory_text.insert(tk.END, f"0x{addr:08X}: 0x{value:08X}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = Segmentado_Stalls_Window(root)
    root.mainloop()
