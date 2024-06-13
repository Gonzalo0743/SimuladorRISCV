import tkinter as tk
from tkinter import ttk, Menu
from gui.uniciclo_window import UnicicloWindow
from gui.pipeline_stalls_window import Segmentado_Stalls_Window
from gui.multiciclo_window import MulticicloWindow
from gui.pipeline_adelantamiento_window import Segmentado_Adelantamiento_Window

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulator RISC-V")
        self.master.geometry("800x600")
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Simulator RISC-V", font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=10)

        # Crear un Frame interno para alinear los botones verticalmente
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(pady=10)

        self.uniciclo_button = tk.Button(self.button_frame, text="Uniciclo", command=self.open_uniciclo, font=("Helvetica", 16))
        self.uniciclo_button.pack(pady=5, padx=10)

        # Añadir botones para los otros procesadores
        self.multiciclo_button = tk.Button(self.button_frame, text="Multiciclo", command=self.open_multiciclo, font=("Helvetica", 16))
        self.multiciclo_button.pack(pady=5, padx=10)

        self.pipeline_button = tk.Button(self.button_frame, text="Pipeline con Stalls", command=self.open_pipeline_stalls, font=("Helvetica", 16))
        self.pipeline_button.pack(pady=5, padx=10)

        self.pipeline_button = tk.Button(self.button_frame, text="Pipeline con Adelantamiento", command=self.open_pipeline_adelantamiento, font=("Helvetica", 16))
        self.pipeline_button.pack(pady=5, padx=10)

        # Añadimos un botón para salir
        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.master.quit, font=("Helvetica", 16))
        self.exit_button.pack(pady=5, padx=10)

    def create_menu(self):
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)

        self.file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)

        self.help_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

    def open_uniciclo(self):
        uniciclo_window = tk.Toplevel(self.master)
        UnicicloWindow(uniciclo_window)

    def open_multiciclo(self):
        multiciclo_window = tk.Toplevel(self.master)
        MulticicloWindow(multiciclo_window)

    def open_pipeline_stalls(self):
        pipeline_stalls_window = tk.Toplevel(self.master)
        Segmentado_Stalls_Window(pipeline_stalls_window)

    def open_pipeline_adelantamiento(self):
        pipeline_adelantamiento_window = tk.Toplevel(self.master)
        Segmentado_Adelantamiento_Window(pipeline_adelantamiento_window)

    def open_file(self):
        # Aquí puedes implementar la lógica para abrir un archivo
        pass

    def show_about(self):
        about_window = tk.Toplevel(self.master)
        about_window.title("About Simulator RISC-V")
        about_window.geometry("400x300")
        label = tk.Label(about_window, text="Simulator RISC-V\nVersion 1.0\nDeveloped by [Tu Nombre]", font=("Helvetica", 14), justify=tk.CENTER)
        label.pack(expand=True, pady=20)
