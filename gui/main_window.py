import tkinter as tk
from processor.uniciclo import Uniciclo

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("RISCV Simulator")
        self.create_widgets()

    def create_widgets(self):
        self.mode_label = tk.Label(self.master, text="Select Processor Mode:")
        self.mode_label.pack()

        self.mode_var = tk.StringVar(value="uniciclo")
        self.uniciclo_radio = tk.Radiobutton(self.master, text="Uniciclo", variable=self.mode_var, value="uniciclo")
        self.uniciclo_radio.pack()
        self.multiciclo_radio = tk.Radiobutton(self.master, text="Multiciclo", variable=self.mode_var, value="multiciclo")
        self.multiciclo_radio.pack()
        self.segmentado_radio = tk.Radiobutton(self.master, text="Segmentado", variable=self.mode_var, value="segmentado")
        self.segmentado_radio.pack()

        self.start_button = tk.Button(self.master, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

        self.output_text = tk.Text(self.master, height=20, width=80)
        self.output_text.pack()

    def start_simulation(self):
        mode = self.mode_var.get()
        if mode == "uniciclo":
            self.simulator = Uniciclo()
        # Implementar los otros modos de simulación aquí
        self.run_simulation()

    def run_simulation(self):
        result = self.simulator.run()
        self.output_text.insert(tk.END, result)
