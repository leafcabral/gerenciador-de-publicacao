"""
ASMbleia
	Ian Caliel Matos Cabral
	João Paulo Pipper da Silva
	Rafael Cabral Lopes
	Vitor Felberg Barcelos
Serra, Brasil
Programa para gerenciamento de banco de dados sobre publicações de livros.

Autora original: Alessandra Aguiar Vilarinho 
"""
import tkinter as tk
from tkinter import ttk

import mod

def main() -> None:
	root = tk.Tk()
	app = mod.MainApplication(root)
	root.mainloop()

if __name__ == "__main__":
	main()
