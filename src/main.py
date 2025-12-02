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

def main() -> None:
	import mod

	app = mod.MainApplication()
	app.root.mainloop()

if __name__ == "__main__":
	main()
