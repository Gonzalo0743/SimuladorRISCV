import tkinter as tk
from tkinter import ttk
from gui.uniciclo_window import UnicicloWindow

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulator RISC-V")
        self.create_widgets()

    def create_widgets(self):
        # Frame para el título
        title_frame = tk.Frame(self.master, pady=10)
        title_frame.pack()
        title_label = tk.Label(title_frame, text="Simulator RISC-V", font=("Helvetica", 16, "bold"))
        title_label.pack()

        # Frame para las opciones de modo
        mode_frame = tk.Frame(self.master, pady=10)
        mode_frame.pack()
        self.mode_label = tk.Label(mode_frame, text="Select Processor Mode:", font=("Helvetica", 12))
        self.mode_label.pack(anchor='w')

        self.mode_var = tk.StringVar(value="uniciclo")

        modes = [("Uniciclo", "uniciclo"), ("Multiciclo", "multiciclo"), ("Segmentado", "segmentado")]
        for text, mode in modes:
            radio = tk.Radiobutton(mode_frame, text=text, variable=self.mode_var, value=mode, font=("Helvetica", 10))
            radio.pack(anchor='w')

        # Frame para el botón de inicio
        button_frame = tk.Frame(self.master, pady=10)
        button_frame.pack()
        self.start_button = tk.Button(button_frame, text="Start Simulation", command=self.open_simulation_window, font=("Helvetica", 12))
        self.start_button.pack()

    def open_simulation_window(self):
        mode = self.mode_var.get()
        if mode == "uniciclo":
            self.new_window(UnicicloWindow)
        # Implementar las ventanas para los otros modos aquí

    def new_window(self, window_class):
        self.new = tk.Toplevel(self.master)
        window_class(self.new)
