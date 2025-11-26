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

def main() -> None:
	try:
		import mysql.connector
	except ModuleNotFoundError:
		print("""
			\rÉ necessário ter o mysql-connector instalado em sua máquina para utilizar esse programa.
			\rUtilize os seguintes comandos para instala-lo, a dependender do seu sistema operacional:
			\r\tWindows: pip install mysql-connector-python
			\r\tLinux: pip3 install mysql-connector
		""")
		return
	
	import mod
	
	root = tk.Tk()
	app = mod.MainApplication(root)
	root.mainloop()

if __name__ == "__main__":
	main()
