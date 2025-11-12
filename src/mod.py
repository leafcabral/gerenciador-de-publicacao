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

import mysql.connector

class InserirDados:
    def __init__(self, parent):
        # FRAME E WINDOW PRINCIPAL
        self.window = tk.Toplevel(parent)
        self.window.title("Inserir uma nova publicação")
        self.window.minsize(400, 300)
        self.window.maxsize(400, 300)
        self.window.resizable(False, False)

        main_frame: ttk.Frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # FRAME DOS INPUTS
        conteudo_frame: ttk.Frame = ttk.Frame(main_frame)
        conteudo_frame.pack(fill=tk.BOTH, expand=True)
        

        # LABEL E INPUT DO ID DO TÍTULO
        id_label: ttk.Label = ttk.Label(conteudo_frame, text="ID do livro:", font=('Arial', 12))
        id_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")

        self.id_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
        self.id_input.grid(row=0, column=1, pady=10, sticky="w")

        self.id_input.bind('<KeyPress>', self.verificar_caractere_ID)
        self.id_input.bind('<KeyRelease>', self.verificar_caractere_ID)

        # LABEL E INPUT DO TÍTULO DO LIVRO

        titulo_label: ttk.Label = ttk.Label(conteudo_frame, text="Título do livro:", font=('Arial', 12))
        titulo_label.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="w")

        self.titulo_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
        self.titulo_input.grid(row=1, column=1, pady=10, sticky="w")

        # LABEL E INPUT DA DATA DO TÍTULO

        data_label: ttk.Label = ttk.Label(conteudo_frame, text="Data de pub. do livro:", font=('Arial', 12))
        data_label.grid(row=2, column=0, padx=(0, 10), pady=10, sticky="w")

        self.data_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
        self.data_input.grid(row=2, column=1, pady=10, sticky="w")

        self.data_input.bind('<KeyPress>', self.verificar_caractere_data)
        self.data_input.bind('<KeyRelease>', self.verificar_caractere_data)

        # LABEL DE ERRO
        self.erro_label: ttk.Label = ttk.Label(conteudo_frame, text="Teste", font=('Arial', 12), foreground="red", wraplength=350, justify="left", anchor="w")
        self.erro_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="we")

        # BOTÕES

        botoes_frame: ttk.Frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X, pady=(20, 0))

        ok_button = ttk.Button(botoes_frame, text="Ok", command=lambda: self.Input(self.id_input,self.titulo_input, self.data_input))
        ok_button.pack(side=tk.RIGHT, padx=(5,0))

        cancelar_button = ttk.Button(botoes_frame, text="Cancelar", command=self.window.destroy)
        cancelar_button.pack(side=tk.RIGHT, padx=(0,5))

    def verificar_caractere_ID(self, event) -> None:
        tam: int = len(self.id_input.get("1.0", "end-1c"))
        LIMITE_CHAR: int = 8

        if tam >= LIMITE_CHAR and event.keysym not in {"BackSpace", "Delete"}:
            return "break"
        
        if not (event.char.isdigit() or event.keysym == "BackSpace"):
            return "break"

    def verificar_caractere_data(self, event) -> None:
        tam: int = len(self.data_input.get("1.0", "end-1c"))
        char_formatacao: list = ['-', ' ', '/']
        LIMITE_CHAR: int = 10

        if tam >= LIMITE_CHAR and event.keysym not in {"BackSpace", "Delete"}:
            return 'break'
        
        if (event.char.isdigit() or event.char in char_formatacao) or event.keysym == "BackSpace":
            return
        
        return "break"

    def verificar_formatacao_data(self, data: str) -> bool:
        i: int = 1
        char_formatacao: list = ['-', ' ', '/']

        # formato correto: yyyy-mm-dd, yyyy mm dd, yyyy/mm/dd
        for char in data:
            if char.isnumeric() and (i <= 4 or (i >= 6 and i < 8) or i >= 9):
                i += 1
            elif char in char_formatacao and (i == 5 or i == 8):
                i += 1
            else:
                return False
        
        if int(data[:4]) == 0 or (int(data[5:7]) == 0 or int(data[5:7]) > 12) or (int(data[9:]) == 0 or int(data[9:]) > 31):
            return False
        
        return True

    def erro(self, texto_erro: str):
        self.erro_label.config(text=texto_erro)

    def Input(self, id_text: tk.Text,titulo: tk.Text, data: tk.Text):
        ID: str = id_text.get("1.0", "end-1c")
        TITULO: str = titulo.get("1.0", "end-1c")
        DATA: str = data.get("1.0", "end-1c")

        if len(ID) == 0 or len(TITULO) == 0 or len(DATA) == 0:
            pass
        elif len(DATA) < 10:
            pass
        elif not self.verificar_formatacao_data(DATA):
            self.erro("Verifique se a formatação da data está correta: yyyy-mm-dd, yyyy mm dd ou yyyy/mm/dd.\nOu então verifique se digitou ano, mês ou dia válido.")
            return

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="publicacao"
        )

        cursor = db.cursor()

        cursor.execute("INSERT INTO titulos (ID_TITULO, TITULO_LIVRO, DATA_PUBLICACAO) VALUES (%s, %s, %s)", (ID, TITULO, DATA))