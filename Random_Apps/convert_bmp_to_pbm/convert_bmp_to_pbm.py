import tkinter as tk
from tkinter import filedialog
from PIL import Image
from tkinter import ttk


class BMPtoPBMConverter:
    def __init__(self, root):
        self.input_file = None
        self.output_folder = None

        self.root = root
        self.root.title("Conversor BMP a PBM")

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", padding=(10, 5))

        frame = ttk.Frame(self.root, padding=10)
        frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Botón para seleccionar la ruta de entrada
        input_button = ttk.Button(
            frame, text="Seleccionar archivo BMP de entrada", command=self.select_input_file)
        input_button.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        self.input_label = ttk.Label(frame, text="Archivo de entrada:")
        self.input_label.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)

        # Botón para seleccionar la ruta de salida
        output_button = ttk.Button(
            frame, text="Seleccionar carpeta de salida", command=self.select_output_folder)
        output_button.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

        self.output_label = ttk.Label(frame, text="Carpeta de salida:")
        self.output_label.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)

        # Botón para iniciar la conversión
        convert_button = ttk.Button(
            frame, text="Convertir BMP a PBM", command=self.convert_bmp_to_pbm)
        convert_button.grid(column=0, row=2, columnspan=2,
                            pady=10, sticky=tk.W)

        # Etiqueta para mostrar el resultado
        self.result_label = ttk.Label(frame, text="")
        self.result_label.grid(
            column=0, row=3, columnspan=2, pady=10, sticky=tk.W)

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename(
            filetypes=[("BMP Files", "*.bmp")])
        self.input_label.config(text=f"Archivo de entrada: {self.input_file}")

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()
        self.output_label.config(
            text=f"Carpeta de salida: {self.output_folder}")

    def convert_bmp_to_pbm(self):
        if self.input_file and self.output_folder:
            name_output = self.input_file.split("/")[-1].split(".bmp")[0]
            output_file = f"{self.output_folder}/{name_output}.pbm"

            try:
                img = Image.open(self.input_file)
                img = img.convert('1')
                img.save(output_file)
                self.result_label.config(
                    text=f"Conversión exitosa: {output_file}")
            except Exception as e:
                self.result_label.config(text=f"Error: {e}")
        else:
            self.result_label.config(
                text="Por favor, selecciona la ruta de entrada y salida primero.")


if __name__ == "__main__":
    root = tk.Tk()
    converter = BMPtoPBMConverter(root)
    root.mainloop()
