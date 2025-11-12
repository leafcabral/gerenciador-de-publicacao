"""
ASMbleia
	Ian Caliel Matos Cabral
	João Paulo Pipper da Silva
	Rafael Cabral Lopes
	Vitor Felberg Barcelos
Serra, Brasil
TODO TODO TODO TODO TODO TODO TODO TODO 
"""

import tkinter as tk
from tkinter import ttk

class InserirDados:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Inserir uma nova publicação")
        self.window.minsize(400, 300)
        self.window.resizable(False, False)

        main_frame: ttk.Frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=False)

        # LABEL E INPUT DO ID DO TÍTULO
        titulo_label: ttk.Label = ttk.Label(main_frame, text="ID do título:", font=('Arial', 12))
        titulo_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")

        self.titulo_input: tk.Text = tk.Text(main_frame, height=1, width=20)
        self.titulo_input.grid(row=0, column=1, pady=10, sticky="w")

        self.titulo_input.bind('<KeyPress>', self.VerificarCaractereID)
        self.titulo_input.bind('<KeyRelease>', self.VerificarCaractereID)

        # LABEL E INPUT DA DATA DO TÍTULO

        data_label: ttk.Label = ttk.Label(main_frame, text="Data do título:", font=('Arial', 12))
        data_label.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="w")

        self.data_input: tk.Text = tk.Text(main_frame, height=1, width=20)
        self.data_input.grid(row=1, column=1, pady=10, sticky="w")

        self.data_input.bind('<KeyPress>', self.VerificarCaractereData)
        self.data_input.bind('<KeyRelease>', self.VerificarCaractereData)

        # BOTÕES:

        cancelar_button = ttk.Button(
            main_frame, 
            text="Cancelar", 
            command=self.window.destroy
        )
        cancelar_button.grid(row=2, column=0, pady=10)

        ok = ttk.Button(
            main_frame, 
            text="Ok", 
            command=lambda: self.Input(self.titulo_input)
        )
        ok.grid(row=2, column=1, pady=10)

    def VerificarCaractereID(self, event):
        tam: int = len(self.titulo_input.get("1.0", "end-1c"))
        LIMITE_CHAR: int = 8

        if tam >= LIMITE_CHAR and event.keysym not in {"BackSpace", "Delete"}:
            return "break"
        
        if not (event.char.isdigit() or event.keysym == "BackSpace"):
            return "break"

    def VerificarCaractereData(self, event):
        tam: int = len(self.titulo_input.get("1.0", "end-1c"))
        LIMITE_CHAR: int = 8

        if tam >= LIMITE_CHAR and event.keysym not in {"BackSpace", "Delete"}:
            return 'break'
        
        if event.char.isdigit() or event.keysym == "BackSpace":
            return
        
        return "break"

    def Input(self, textbox: tk.Text):
        INPUT: str = textbox.get("1.0", "end-1c")

        print(INPUT)