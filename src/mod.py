"""
ASMbleia
	Ian Caliel Matos Cabral
	João Paulo Pipper da Silva
	Rafael Cabral Lopes
	Vitor Felberg Barcelos
Serra, Brasil
Programa para gerenciamento de banco de dados sobre publicações de livros.

Classe MainApplication originalmente por: Alessandra Aguiar Vilarinho.
"""
import tkinter as tk
from tkinter import ttk

import mysql.connector

from webbrowser import open_new

class MainApplication:
	def __init__(self, root):
		self.root = root
		self.root.title("Gerenciador de Publicações")
		self.root.geometry("800x600")

		self.root.minsize(800, 600)
		
		# Criar database pelo arquivo, se não existir
		self.init_db("publicacao", "res/sql/BDPublicacao.sql")

		# Configurar o menu principal
		self.setup_menu()
		
		# Conteúdo da janela principal
		self.setup_content()
	
	def init_db(self, name: str, file_name: str):
		db = mysql.connector.connect(
			host="localhost",
			user="root",
			password="serra"
		)
		cursor = db.cursor()
		cursor.execute(
			"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
			(name, )
		)

		if not cursor.fetchone():
			with open(file_name, "r", encoding="utf-8") as script:
				cursor.execute(script.read(), multi=True)

	def setup_content(self):
		# Frame principal
		main_frame = ttk.Frame(self.root, padding="10")
		main_frame.pack(fill=tk.BOTH, expand=True)
		
		# Título
		title_label = ttk.Label(
			main_frame, 
			text="Bem-vindo(a) ao Gerenciador de Publicações!", 
			font=('Arial', 16, 'bold')
		)
		title_label.pack()
		
		# Descrição
		desc_label = ttk.Label(
			main_frame, 
			text="Lorem ipsum",
			font=('Arial', 12, 'bold')
		)
		desc_label.pack(pady=20)
		
		# Rodapé
		footer_label = ttk.Label(
			main_frame, 
			text="Lorem ipsum",
			font=('Arial', 10, 'bold')
		)
		footer_label.pack(side=tk.BOTTOM, pady=10)
	
	def setup_menu(self):
		# Criar a barra de menu
		menubar = tk.Menu(self.root)
		self.root.config(menu=menubar)
		
		# Menu Empregado
		file_menu = tk.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Banco de dados", menu=file_menu)
		file_menu.add_command(
			label="Inserir uma publicação", 
			command=lambda: InserirDados(self.root)
		)
		file_menu.add_separator()
		file_menu.add_command(
			label="Alterar uma publicação", 
			command=lambda: AlterarDados(self.root)
		)
		file_menu.add_separator()
		file_menu.add_command(
			label="Excluir uma publicação", 
			command=lambda: DeletarDados(self.root)
		)
		file_menu.add_separator()
		file_menu.add_command(
			label="Consultar publicação por critério", 
			command=lambda: ChildWindow(self.root, "Consultar por critério", "Aqui entra sua janela com\n\n\nlógica para consultar um empregado por um critério")
		)
		file_menu.add_separator()
		file_menu.add_command(
			label="Consultar todas as publiações", 
			command=lambda: ChildWindow(self.root, "Consultar todos", "Aqui entra sua janela com\n\n\nlógica para consultar todos empregados")
		)
		file_menu.add_separator()
		file_menu.add_command(label="Sair", command=self.root.quit)
		
		# Menu Ajuda
		help_menu = tk.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Ajuda", menu=help_menu)
		help_menu.add_command(
			label="Como usar o Gerenciador", 
			command=lambda: ChildWindow(self.root, "Terminando as disciplinas de programação com a profa. Alessandra.", "Adeus Programação em Python")
		)
		help_menu.add_separator()
		help_menu.add_command(label="Sobre a aplicação", command=self.show_about)
	
	def show_about(self):
		from tkinter import font

		about_window = tk.Toplevel(self.root)
		about_window.title("Sobre a aplicação")
		about_window.geometry("350x350")
		about_window.resizable(False, False)

		main_frame: ttk.Frame = ttk.Frame(about_window, padding=10)
		main_frame.pack(fill=tk.BOTH, expand=True)

		fonte_underline: font.Font = font.Font(family="Arial", size=10, underline=True)
		
		# FRAME E LABELS SUPERIORES
		labels_superiores_frame: ttk.Frame = ttk.Frame(main_frame)
		labels_superiores_frame.pack(fill=tk.BOTH, expand=True)

		ttk.Label(labels_superiores_frame, text="Gerenciador de Publicações", font=('Arial', 14)).pack()
		ttk.Label(labels_superiores_frame, text="Versão 1.0").pack()
		ttk.Label(labels_superiores_frame, text="Desenvolvido por ASMbleia.").pack()
		ttk.Label(labels_superiores_frame, text="Autora original: Alessandra Aguiar.").pack(pady=(0, 50))

		# FRAME E LABELS INFERIORES
		labels_inferiores_frame: ttk.Frame = ttk.Frame(main_frame)
		labels_inferiores_frame.pack(fill=tk.X, pady=(20,0))

		ttk.Label(labels_inferiores_frame, text="Este software vem com nenhuma garantia.").pack()

		label_licenca: ttk.Label = ttk.Label(labels_inferiores_frame, text="Licença: GPLv3.0", font=fonte_underline, foreground="blue", cursor="hand2")

		label_licenca.bind("<Button-1>", lambda e: open_new("https://www.gnu.org/licenses/gpl-3.0.en.html"))
		label_licenca.pack()

		label_source: ttk.Label = ttk.Label(labels_inferiores_frame, text="Acessar código-fonte",font=fonte_underline, foreground="blue", cursor="hand2")

		label_source.bind("<Button-1>", lambda e: open_new("https://github.com/leafcabral/nome-temporario"))
		label_source.pack()

class InserirDados:
	def __init__(self, parent):
		# FRAME E WINDOW PRINCIPAL
		self.window = tk.Toplevel(parent)
		self.window.title("Inserir uma nova publicação")
		self.window.minsize(400, 350)
		self.window.maxsize(400, 350)
		self.window.resizable(False, False)

		main_frame: ttk.Frame = ttk.Frame(self.window, padding="10")
		main_frame.pack(fill=tk.BOTH, expand=True)

		# FRAME DOS INPUTS
		conteudo_frame: ttk.Frame = ttk.Frame(main_frame)
		conteudo_frame.pack(fill=tk.BOTH, expand=True)

		# LABEL E INPUT DO ID DO LIVRO
		id_label: ttk.Label = ttk.Label(conteudo_frame, text="ID do livro:", font=('Arial', 12))
		id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

		self.id_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
		self.id_input.grid(row=0, column=1, pady=10, sticky="w")

		self.id_input.bind('<KeyPress>', self.verificar_caractere_ID)
		self.id_input.bind('<KeyRelease>', self.verificar_caractere_ID)

		# LABEL E INPUT DO TÍTULO DO LIVRO
		titulo_label: ttk.Label = ttk.Label(conteudo_frame, text="Título do livro:", font=('Arial', 12))
		titulo_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

		self.titulo_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
		self.titulo_input.grid(row=1, column=1, pady=10, sticky="w")

		self.titulo_input.bind('<KeyPress>', self.verificar_caractere_titulo)
		self.titulo_input.bind('<KeyRelease>', self.verificar_caractere_titulo)

		# LABEL E INPUT DO TIPO DO LIVRO
		tipo_label: ttk.Label = ttk.Label(conteudo_frame, text="Tipo de livro:", font=('Arial', 12))
		tipo_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

		self.tipo_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
		self.tipo_input.grid(row=2, column=1, pady=10, sticky="w")

		self.tipo_input.bind('<KeyPress>', self.verificar_caractere_tipo)
		self.tipo_input.bind('<KeyRelease>', self.verificar_caractere_tipo)

		# LABEL E INPUT DA DATA DO LIVRO
		data_label: ttk.Label = ttk.Label(conteudo_frame, text="Data de pub. do livro:", font=('Arial', 12))
		data_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

		self.data_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
		self.data_input.grid(row=3, column=1, pady=10, sticky="w")

		self.data_input.bind('<KeyPress>', self.verificar_caractere_data)
		self.data_input.bind('<KeyRelease>', self.verificar_caractere_data)

		# LABEL DE ERRO
		self.erro_label: ttk.Label = ttk.Label(conteudo_frame, text="", font=('Arial', 12), foreground="red", wraplength=350, justify="left", anchor="w")
		self.erro_label.grid(row=4, column=0, columnspan=2, pady=10, sticky="we")

		# BOTÕES
		botoes_frame: ttk.Frame = ttk.Frame(main_frame)
		botoes_frame.pack(fill=tk.X, pady=(20, 0))

		ok_button = ttk.Button(botoes_frame, text="Ok", command=lambda: self.input(self.id_input,self.titulo_input, self.tipo_input, self.data_input))
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

	def verificar_caractere_titulo(self, event) -> None:
		tam: int = len(self.titulo_input.get("1.0", "end-1c"))
		LIMITE_CHAR: int = 80

		if tam >= LIMITE_CHAR and event.keysym not in {"BackSpace", "Delete"}:
			return 'break'
	
	def verificar_caractere_tipo(self, event) -> None:
		tam: int = len(self.tipo_input.get("1.0", "end-1c"))
		LIMITE_CHAR: int = 12

		if tam >= LIMITE_CHAR and event.keysym not in {"BackSpace", "Delete"}:
			return 'break'

	def verificar_formatacao_data(self, data: str) -> bool:
		i: int = 1
		char_formatacao: list = ['-', ' ', '/']

		if len(data) != 10:
			return False

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

	def input(self, id_text: tk.Text,titulo: tk.Text, tipo: tk.Text, data: tk.Text):
		ID: str = id_text.get("1.0", "end-1c")
		TITULO: str = titulo.get("1.0", "end-1c").strip()
		TIPO: str = tipo.get("1.0", "end-1c").strip()
		DATA: str = data.get("1.0", "end-1c")

		if len(ID) == 0 or len(TITULO) == 0 or len(TIPO) == 0 or len(DATA) == 0:
			self.erro("Dados inválidos: algum(ns) campo(s) está(ão) vazio(s)")
			return
		elif not self.verificar_formatacao_data(DATA):
			self.erro("Verifique se a formatação da data está correta: yyyy-mm-dd, yyyy mm dd ou yyyy/mm/dd.\nOu então verifique se digitou ano, mês ou dia válido.")
			return

		db = mysql.connector.connect(
			host="localhost",
			user="root",
			password="serra",
			database="publicacao"
		)

		cursor = db.cursor()

		cursor.execute("INSERT INTO titulos (ID_TITULO, TITULO_LIVRO, TIPO_LIVRO, DATA_PUBLICACAO) VALUES (%s, %s, %s, %s)", (ID, TITULO, TIPO, DATA))
		db.commit()

class AlterarDados:
	def __init__(self, parent):
		# FRAME E WINDOW PRINCIPAL
		self.window = tk.Toplevel(parent)
		self.window.title("Alterar uma publicação")
		self.window.minsize(400, 350)
		self.window.maxsize(400, 350)
		self.window.resizable(False, False)

		main_frame: ttk.Frame = ttk.Frame(self.window, padding="10")
		main_frame.pack(fill=tk.BOTH, expand=True)

		# FRAME DOS INPUTS
		conteudo_frame: ttk.Frame = ttk.Frame(main_frame)
		conteudo_frame.pack(fill=tk.BOTH, expand=True)

		# LABEL E INPUT DO ID DO LIVRO
		id_label: ttk.Label = ttk.Label(conteudo_frame, text="ID do livro*:", font=('Arial', 12))
		id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

		self.id_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
		self.id_input.grid(row=0, column=1, pady=10, sticky="w")

		self.id_input.bind('<KeyPress>', self.verificar_caractere_ID)
		self.id_input.bind('<KeyRelease>', self.verificar_caractere_ID)

		# LABEL E INPUT DO TÍTULO DO LIVRO
		titulo_label: ttk.Label = ttk.Label(conteudo_frame, text="Título do livro:", font=('Arial', 12))
		titulo_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

		self.titulo_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
		self.titulo_input.grid(row=1, column=1, pady=10, sticky="w")

		self.titulo_input.bind('<KeyPress>', self.verificar_caractere_titulo)
		self.titulo_input.bind('<KeyRelease>', self.verificar_caractere_titulo)

		# LABEL E INPUT DO TIPO DO LIVRO
		tipo_label: ttk.Label = ttk.Label(conteudo_frame, text="Tipo de livro:", font=('Arial', 12))
		tipo_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

		self.tipo_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
		self.tipo_input.grid(row=2, column=1, pady=10, sticky="w")

		self.tipo_input.bind('<KeyPress>', self.verificar_caractere_tipo)
		self.tipo_input.bind('<KeyRelease>', self.verificar_caractere_tipo)

		# LABEL E INPUT DA DATA DO LIVRO
		data_label: ttk.Label = ttk.Label(conteudo_frame, text="Data de pub. do livro:", font=('Arial', 12))
		data_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

		self.data_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
		self.data_input.grid(row=3, column=1, pady=10, sticky="w")

		self.data_input.bind('<KeyPress>', self.verificar_caractere_data)
		self.data_input.bind('<KeyRelease>', self.verificar_caractere_data)

		# LABEL DE ERRO
		self.erro_label: ttk.Label = ttk.Label(conteudo_frame, text="", font=('Arial', 12), foreground="red", wraplength=350, justify="left", anchor="w")
		self.erro_label.grid(row=4, column=0, columnspan=2, pady=10, sticky="we")

		# BOTÕES
		botoes_frame: ttk.Frame = ttk.Frame(main_frame)
		botoes_frame.pack(fill=tk.X, pady=(20, 0))

		ok_button = ttk.Button(botoes_frame, text="Ok", command=lambda: self.input(self.id_input,self.titulo_input, self.tipo_input, self.data_input))
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

	def verificar_caractere_titulo(self, event) -> None:
		tam: int = len(self.titulo_input.get("1.0", "end-1c"))
		LIMITE_CHAR: int = 80

		if tam >= LIMITE_CHAR and event.keysym not in {"BackSpace", "Delete"}:
			return 'break'
	
	def verificar_caractere_tipo(self, event) -> None:
		tam: int = len(self.tipo_input.get("1.0", "end-1c"))
		LIMITE_CHAR: int = 12

		if tam >= LIMITE_CHAR and event.keysym not in {"BackSpace", "Delete"}:
			return 'break'

	def verificar_formatacao_data(self, data: str) -> bool:
		i: int = 1
		char_formatacao: list = ['-', ' ', '/']

		if len(data) != 10:
			return False

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

	def input(self, id_text: tk.Text,titulo: tk.Text, tipo: tk.Text, data: tk.Text):
		ID: str = id_text.get("1.0", "end-1c")
		TITULO: str = titulo.get("1.0", "end-1c").strip()
		TIPO: str = tipo.get("1.0", "end-1c").strip()
		DATA: str = data.get("1.0", "end-1c")

		if len(ID) == 0:
			self.erro("Digite ID do livro que deseja alterar.")
			return
		elif len(TITULO) == 0 and len(TIPO) == 0 and len(DATA) == 0:
			self.erro("Dados inválidos: todos os campos estão vazios")
			return
		elif len(DATA) > 0 and not(self.verificar_formatacao_data(DATA)):
			self.erro("Verifique se a formatação da data está correta: yyyy-mm-dd, yyyy mm dd ou yyyy/mm/dd.\nOu então verifique se digitou ano, mês ou dia válido.")
			return

		db = mysql.connector.connect(
			host="localhost",
			user="root",
			password="serra",
			database="publicacao"
		)

		cursor = db.cursor()

		comando: str = "UPDATE titulos SET "

		dados: dict = {
			TITULO : "TITULO_LIVRO = ",
			TIPO : "TIPO_LIVRO = ",
			DATA : "DATA_PUBLICACAO = "
		}

		for (chave, valor) in dados.items():
			if len(chave) > 0:
				comando += valor + f"\'{chave}\',"

		comando = comando[:-1]
		comando += f" WHERE ID_TITULO = {ID}"

		cursor.execute(comando)
		db.commit()

class DeletarDados:
	def __init__(self, parent):
		# FRAME E WINDOW PRINCIPAL
		self.window = tk.Toplevel(parent)
		self.window.title("Deletar uma publicação")
		self.window.minsize(400, 350)
		self.window.maxsize(400, 350)
		self.window.resizable(False, False)

		main_frame: ttk.Frame = ttk.Frame(self.window, padding="10")
		main_frame.pack(fill=tk.BOTH, expand=True)

		# FRAME DOS INPUTS
		conteudo_frame: ttk.Frame = ttk.Frame(main_frame)
		conteudo_frame.pack(fill=tk.BOTH, expand=True)

		# LABEL E INPUT DO ID DO LIVRO
		id_label: ttk.Label = ttk.Label(conteudo_frame, text="ID do livro*:", font=('Arial', 12))
		id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

		self.id_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
		self.id_input.grid(row=0, column=1, pady=10, sticky="w")

		self.id_input.bind('<KeyPress>', self.verificar_caractere_ID)
		self.id_input.bind('<KeyRelease>', self.verificar_caractere_ID)

		# LABEL E INPUT DO TÍTULO DO LIVRO
		titulo_label: ttk.Label = ttk.Label(conteudo_frame, text="Título do livro:", font=('Arial', 12))
		titulo_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

		self.titulo_input: tk.Text = tk.Text(conteudo_frame, height=1, width=20)
		self.titulo_input.grid(row=1, column=1, pady=10, sticky="w")

		self.titulo_input.bind('<KeyPress>', self.verificar_caractere_titulo)
		self.titulo_input.bind('<KeyRelease>', self.verificar_caractere_titulo)

		# BOTÃO RADIO
		radio_frame: ttk.Frame = ttk.Frame(main_frame)
		radio_frame.pack(fill=tk.X, pady=(20, 0))

		self.radio_value = tk.StringVar(radio_frame, "ID")

		radio_values = {"Deletar via ID" : "ID", 
        		"Deletar via nome" : "Nome"} 

		for (text, value) in radio_values.items(): 
			ttk.Radiobutton(radio_frame, text = text, variable = self.radio_value, value = value).pack(side = 'top', ipady = 5) 

		# LABEL DE ERRO
		self.erro_label: ttk.Label = ttk.Label(conteudo_frame, text="", font=('Arial', 12), foreground="red", wraplength=350, justify="left", anchor="w")
		self.erro_label.grid(row=4, column=0, columnspan=2, pady=10, sticky="we")

		# BOTÕES
		botoes_frame: ttk.Frame = ttk.Frame(main_frame)
		botoes_frame.pack(fill=tk.X, pady=(20, 0))

		ok_button = ttk.Button(botoes_frame, text="Ok", command=lambda: self.input(self.id_input,self.titulo_input))
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

	def verificar_caractere_titulo(self, event) -> None:
		tam: int = len(self.titulo_input.get("1.0", "end-1c"))
		LIMITE_CHAR: int = 80

		if tam >= LIMITE_CHAR and event.keysym not in {"BackSpace", "Delete"}:
			return 'break'

	def erro(self, texto_erro: str):
		self.erro_label.config(text=texto_erro)

	def input(self, id_text: tk.Text,titulo: tk.Text):
		ID: str = id_text.get("1.0", "end-1c")
		TITULO: str = titulo.get("1.0", "end-1c").strip()
		if self.radio_value.get() == "ID":
			if len(ID) == 0:
				self.erro("Digite o ID do livro que deseja alterar.")
				return
		else:
			if len(TITULO) == 0:
				self.erro("Digite o nome do livro que deseja alterar.")
				return
			
		self.erro("")

		db = mysql.connector.connect(
			host="localhost",
			user="root",
			password="serra",
			database="publicacao"
		)

		cursor = db.cursor()

		comando: str = "SET FOREIGN_KEY_CHECKS = 0;DELETE FROM titulos"

		if self.radio_value.get() == "ID":
			comando += f" WHERE ID_TITULO = {ID}"
		else:
			comando += f" WHERE TITULO_LIVRO = {TITULO};SET FOREIGN_KEY_CHECKS = 1;"

		cursor.execute(comando)
		db.commit()