import tkinter as tk
from processor.uniciclo import Uniciclo

class UnicicloWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Uniciclo Simulator")
        self.create_widgets()
        self.simulator = Uniciclo()

    def create_widgets(self):
        # Frame para el título
        title_frame = tk.Frame(self.master, pady=10)
        title_frame.pack()
        title_label = tk.Label(title_frame, text="Uniciclo Simulator", font=("Helvetica", 16, "bold"))
        title_label.pack()

        # Frame para el botón de carga de programa
        button_frame = tk.Frame(self.master, pady=10)
        button_frame.pack()
        self.load_button = tk.Button(button_frame, text="Load Program", command=self.load_program, font=("Helvetica", 12))
        self.load_button.pack()

        # Frame para el botón de inicio
        self.start_button = tk.Button(button_frame, text="Start Simulation", command=self.start_simulation, font=("Helvetica", 12))
        self.start_button.pack()

        # Frame para el botón de paso a paso
        self.step_button = tk.Button(button_frame, text="Step", command=self.step_simulation, font=("Helvetica", 12))
        self.step_button.pack()

        # Frame para la salida de texto
        output_frame = tk.Frame(self.master, pady=10)
        output_frame.pack()
        self.output_text = tk.Text(output_frame, height=20, width=80, font=("Courier", 10))
        self.output_text.pack()

        # Frame para la visualización de memoria
        memory_frame = tk.Frame(self.master, pady=10)
        memory_frame.pack()
        self.memory_button = tk.Button(memory_frame, text="Show Memory", command=self.show_memory, font=("Helvetica", 12))
        self.memory_button.pack()

    def load_program(self):
        # Cargar un programa ejemplo en el simulador
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

    def start_simulation(self):
        self.output_text.delete('1.0', tk.END)
        result = self.simulator.run()
        self.output_text.insert(tk.END, result)

    def step_simulation(self):
        result = self.simulator.step()
        self.output_text.insert(tk.END, result)

    def show_memory(self):
        memory_content = self.simulator.display_memory()
        self.output_text.insert(tk.END, memory_content)
