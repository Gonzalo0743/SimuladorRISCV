import tkinter as tk
from processor.multiciclo import Multiciclo
from processor.assembler import Assembler
from processor.execution_statistics import ExecutionStatistics
import time

class MulticicloWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Multicycle Simulator")
        self.create_widgets()
        self.simulator = Multiciclo()
        self.assembler = Assembler()
        self.start_time = None
        self.execution_time = 0
        self.execution_stats = ExecutionStatistics()
        self.cycle_time_ns = 10  # Suponiendo 10 ns por ciclo
        self.num_instructions = 0

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

        self.cpi_label = tk.Label(self.status_frame, text="CPI: 0")
        self.cpi_label.pack(side=tk.LEFT, padx=5)

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

        self.stats_label = tk.Label(self.data_frame, text="Statistics", font=("Helvetica", 14))
        self.stats_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.stats_text = tk.Text(self.data_frame, height=10, width=80)
        self.stats_text.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    def load_program(self):
        assembly_code = self.assembly_text.get("1.0", tk.END)
        try:
            machine_code = self.assembler.assemble(assembly_code)
            self.simulator.load_program(machine_code)
            self.num_instructions = len(machine_code)
            self.output_text.insert(tk.END, "Assembly program loaded.\n")
        except ValueError as e:
            self.output_text.insert(tk.END, f"Error: {e}\n")

    def run_program(self):
        if self.start_time is None:
            self.start_time = time.time()
        while self.simulator.pc < len(self.simulator.memory) and self.simulator.running:
            output = self.simulator.step()
            self.execution_time = time.time() - self.start_time
            self.update_ui()
            self.output_text.insert(tk.END, output)
        self.record_statistics()
        if not self.simulator.running:
            self.output_text.insert(tk.END, "Program execution stopped by ebreak.\n")
        else:
            self.output_text.insert(tk.END, "Program execution finished.\n")

    def run_timed_program(self):
        if self.start_time is None:
            self.start_time = time.time()
        self.master.after(1000, self.step_timed)

    def step_timed(self):
        if self.uniciclo.pc < len(self.uniciclo.memory) and self.uniciclo.running:
            output = self.simulator.step()
            self.execution_time = time.time() - self.start_time
            self.update_ui()
            self.output_text.insert(tk.END, output)
            self.master.after(1000, self.step_timed)
        else:
            self.record_statistics()
            if not self.uniciclo.running:
                self.output_text.insert(tk.END, "Program execution stopped by ebreak.\n")
            else:
                self.output_text.insert(tk.END, "Program execution finished.\n")

    def step_program(self):
        if self.start_time is None:
            self.start_time = time.time()
        if self.uniciclo.pc < len(self.uniciclo.memory) and self.uniciclo.running:
            output = self.simulator.step()
            self.execution_time = time.time() - self.start_time
            self.update_ui()
            self.output_text.insert(tk.END, output)
        else:
            self.record_statistics()
            if not self.uniciclo.running:
                self.output_text.insert(tk.END, "Program execution stopped by ebreak.\n")
            else:
                self.output_text.insert(tk.END, "Program execution finished.\n")

    def record_statistics(self):
        num_cycles = self.simulator.cycle_count
        num_instructions = self.num_instructions  # Corregido: usamos la longitud del programa cargado
        cpi = num_cycles / num_instructions
        execution_time_ns = num_cycles * self.cycle_time_ns
        self.execution_stats.add_execution(num_cycles, num_instructions, self.cycle_time_ns)
        self.display_statistics()

    def display_statistics(self):
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert(tk.END, f"{'Execution':<10}{'Cycles':<10}{'Instructions':<15}{'CPI':<10}{'Time (ns)':<10}\n")
        for i, stat in enumerate(self.execution_stats.get_statistics()):
            self.stats_text.insert(tk.END, f"{i+1:<10}{stat['num_cycles']:<10}{stat['num_instructions']:<15}{stat['cpi']:<10}{stat['execution_time_ns']:<10}\n")

    def update_ui(self):
        self.cycle_label.config(text=f"Cycle: {self.simulator.cycle_count}")
        self.time_label.config(text=f"Execution Time: {self.execution_time:.2f}s")
        self.pc_label.config(text=f"PC: 0x{self.simulator.pc:08X}")
        self.update_registers()
        self.update_memory()

    def update_registers(self):
        self.registers_text.delete('1.0', tk.END)
        for i in range(len(self.simulator.registers)):
            self.registers_text.insert(tk.END, f"x{i}: 0x{self.simulator.registers[i]:08X}\n")

    def update_memory(self):
        self.memory_text.delete('1.0', tk.END)
        for addr in range(0, len(self.simulator.memory), 4):
            value = int.from_bytes(self.simulator.memory[addr:addr + 4], byteorder='little')
            self.memory_text.insert(tk.END, f"0x{addr:08X}: 0x{value:08X}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MulticicloWindow(root)
    root.mainloop()