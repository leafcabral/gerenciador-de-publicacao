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

class DatabaseManager:
	def __init__(self, host: str, user: str, password: str, database: str):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.connection = None
	#end_def

	def connect(self):
		self.connection = mysql.connector.connect(
			host=self.host,
			user=self.user,
			password=self.password
		)
		cursor = self.connection.cursor()
		cursor.execute(
			"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = %s",
			(self.database, )
		)

		if not cursor.fetchone():
			with open(f"res/sql/BD{self.database.capitalize()}.sql", "r", encoding="utf-8") as script:
				cursor.execute(script.read(), multi=True)

		self.connection.database = self.database
	#end_def

	def disconnect(self) -> None:
		if self.connection:
			self.connection.close()
			self.connection = None
	#end_def

	def execute_query(self, query: str, params: tuple = ()) -> list:
		cursor = self.connection.cursor()
		cursor.execute(query, params)

		query_clause = query.strip().upper()
		if query_clause.startswith("SELECT") or query_clause.startswith("SHOW"):
			result = cursor.fetchall()
			cursor.close()
			return result
		else:
			self.connection.commit()
			cursor.close()
			return []
	#end_def

	def inserir_publicacao(self, id: str, titulo: str, tipo: str, data: str) -> bool:
		query = "INSERT INTO titulos (ID_TITULO, TITULO_LIVRO, TIPO_LIVRO, DATA_PUBLICACAO) VALUES (%s, %s, %s, %s)"
		check_query = "SELECT * FROM titulos WHERE ID_TITULO = %s"

		if not self.execute_query(check_query, (id, )):
			self.execute_query(query, (id, titulo, tipo, data))
			return True
		else:
			return False
	#end_def

	def alterar_publicacao(self, id: str, titulo: str = "", tipo: str = "", data: str = "") -> bool:
		fields = []
		params = []

		if titulo:
			fields.append("TITULO_LIVRO = %s")
			params.append(titulo.strip())
		if tipo:
			fields.append("TIPO_LIVRO = %s")
			params.append(tipo.strip())
		if data:
			fields.append("DATA_PUBLICACAO = %s")
			params.append(data.strip())

		if not fields:
			return False
		params.append(id)
		query = f"UPDATE titulos SET {', '.join(fields)} WHERE ID_TITULO = %s"
		self.execute_query(query, tuple(params))
		return True
	#end_def

	def deletar_publicacao(self, id: str, titulo: str, pelo_id: bool) -> bool:
		self.execute_query("SET FOREIGN_KEY_CHECKS = 0")
		where_clause = f"ID_TITULO = '{id.strip()}'" if pelo_id else f"TITULO_LIVRO = {titulo.strip()}'"
		query = f"DELETE FROM titulos WHERE {where_clause}"
		check_query = f"SELECT * FROM titulos WHERE {where_clause}"

		if self.execute_query(check_query):
			self.execute_query(query)
			self.execute_query("SET FOREIGN_KEY_CHECKS = 1")
			return True
		else:
			self.execute_query("SET FOREIGN_KEY_CHECKS = 1")
			return False
	#end_def

	def consultar_todas_publicacoes(self) -> list:
		query = "SELECT * FROM titulos"
		return self.execute_query(query)
	#end_def

	def consultar_por_criterio(self, criterio: list) -> list:
		ID: str = criterio[0]
		NOME: str = criterio[1]
		DATA: list = criterio[2]

		query: str = "SELECT * FROM titulos WHERE "

		if len(ID) > 0: query += f"ID_TITULO = {ID},"
		if len(NOME) > 0: query += f" TITULO_LIVRO = {NOME},"
		if len(DATA[0]) > 0: query += f" DATA_PUBLICACAO BETWEEN {DATA[0]} AND {DATA[1]},"

		query = query[:-1]

		return self.execute_query(query)
	#end_def

#end_class

class GraphicsManager:
	def __init__(self, root, main_app):
		self.root = root
		self.main_app = main_app
		self.root.title("Gerenciador de Publicações")
		self.root.geometry("800x600")
		self.root.minsize(800, 600)
		root.state('zoomed')
		root.iconphoto(True, tk.PhotoImage(file='res/icon.png'))
		
		self.setup_navbar()
		self.setup_content()
		self.status = {
			'user': 'Conectado',
			'database': 'publicacao'
		}
		self.statusbar = self.setup_statusbar()

		style = ttk.Style()
		root.tk.call('source', 'res/forest-light.tcl')
		style.theme_use('forest-light')
		style.configure('.', font=('Segoe UI', 12))
	#end_def

	def setup_navbar(self):
		menubar = tk.Menu(self.root)
		self.root.config(menu=menubar)
		
		arq_menu = tk.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Arquivo", menu=arq_menu)
		arq_menu.add_command(label="Sair", command=self.root.quit)

		titulo_menu = tk.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Título", menu=titulo_menu)
		titulo_menu.add_command(
			label="Inserir título",
			command=self.main_app.inserir_titulo
		)
		titulo_menu.add_command(
			label="Alterar título",
			command=self.main_app.alterar_titulo
		)
		titulo_menu.add_command(
			label="Excluir título",
			command=self.main_app.excluir_titulo
		)
		titulo_menu.add_separator()
		titulo_menu.add_command(
			label="Consultar todos os títulos",
			command=self.main_app.consultar_titulos
		)
		titulo_menu.add_command(
			label="Consultar título por critério",
			command=self.main_app.consultar_titulo_criterio
		)

		ajuda_menu = tk.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Ajuda", menu=ajuda_menu)
		ajuda_menu.add_command(
			label="Como usar o Gerenciador", 
			command=self.main_app.mostrar_ajuda
		)
		ajuda_menu.add_separator()
		ajuda_menu.add_command(
			label="Mostrar informações de licença",
			command=self.main_app.mostrar_licenca
		)
		ajuda_menu.add_command(
			label="Sobre a aplicação",
			command=self.main_app.mostrar_sobre
		)
	#end_def

	def setup_content(self):
		main_frame = ttk.Frame(self.root, padding="10")
		main_frame.pack(fill=tk.BOTH, expand=True)
		
		header_frame = ttk.Frame(main_frame)
		header_frame.pack(fill=tk.X, pady=(0,20))

		title_label = ttk.Label(
			header_frame,
			text="Gerenciador de Publicações",
			font=('Segoe UI', 28, 'bold'),
			foreground='#333333'
		)
		subtitle = ttk.Label(
			header_frame,
			text="Sistema de gerenciamento de banco de dados de livros",
		)
		title_label.pack()
		subtitle.pack(pady=(0, 50))

		welcome_frame = ttk.LabelFrame(
			main_frame,
			text="Seja bem-vindo!",
			padding=(10, 0, 10, 10),
			labelanchor='n',
		)
		welcome_text = ttk.Label(
			welcome_frame,
# Se colocar tab no texto, o tkinter salta muito mais espaço 
			text="""Use o menu de navegação para gerenciar suas publicações:\n
• Inserir novos títulos
• Alterar informações existentes
• Excluir registros
• Consultar dados""",
			justify=tk.LEFT
		)
		# welcome_frame.pack(fill=tk.X, padx=700, pady=(0, 20), anchor=tk.CENTER)
		welcome_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
		welcome_text.pack()

		footer_label = ttk.Label(
			main_frame,
			text="COPYLEFT 2025 ASMbleia • Desenvolvido por Ian, João, Rafael, Vitor • Serra, Brasil",
		)
		footer_label.pack(side=tk.BOTTOM, pady=10)
	#end_def

	def setup_statusbar(self):
		statusbar = ttk.Label(
			self.root,
			text=f"  Usuário: {self.status['user']} | Banco de Dados: {self.status['database']}",
			relief=tk.SUNKEN,
			anchor=tk.W,
			background="#f0f0f0"
		)
		statusbar.pack(side=tk.BOTTOM, fill=tk.X, ipady=2)
		return statusbar
	#end_def

	def create_window(self, title: str, size: str = "400x300", resizable: bool = False) -> tk.Toplevel:
		window = tk.Toplevel(self.root)
		window.title(title)
		window.geometry(size)

		window.resizable(True, True)
		if not resizable:
			width, height = map(int, size.split('x'))
			window.minsize(width, height)
			window.maxsize(width, height)

			window.resizable(False, False)
		return window
	#end_def
	def create_frame(self, parent, padding: int = 10) -> ttk.Frame:
		frame = ttk.Frame(parent, padding=padding)
		return frame
	#end_def
	def create_entry(self, parent, width: int = 20) -> tk.Text:
		return tk.Text(parent, height=1, width=width)
	#end_def
	def create_label(self, parent, text: str, font: tuple = ('Arial', 12)) -> ttk.Label:
		return ttk.Label(parent, text=text, font=font)
	#end_def
	def create_button(self, parent, text: str, command) -> ttk.Button:
		return ttk.Button(parent, text=text, command=command)
	#end_def
#end_class

class MainApplication:
	def __init__(self, root):
		self.root = root

		self.graphics_manager = GraphicsManager(self.root, self)

		input_user_senha = self.graphics_manager.create_window("Banco de dados")

		main_frame = self.graphics_manager.create_frame(input_user_senha)
		main_frame.pack(fill=tk.BOTH, expand=True)
		main_frame.grid_rowconfigure(3, weight=1)
		main_frame.grid_columnconfigure(0, weight=1)

		user_label = self.graphics_manager.create_label(main_frame, "Digite seu usuário:")
		user_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
		user_input = self.graphics_manager.create_entry(main_frame)
		user_input.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

		senha_label = self.graphics_manager.create_label(main_frame, "Digite sua senha:")
		senha_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
		senha_input = self.graphics_manager.create_entry(main_frame)
		senha_input.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

		erro_label = self.graphics_manager.create_label(main_frame, "", font=('Arial', 12))
		erro_label.config(wraplength=350, justify="left", anchor="w")
		erro_label.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

		botao_frame = self.graphics_manager.create_frame(main_frame)
		botao_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="se")
		botao = self.graphics_manager.create_button(botao_frame, "Ok", command=lambda:
			self.verificar_user_senha(user_input, senha_input, erro_label, input_user_senha)
		)
		botao.pack(side=tk.RIGHT, padx=(5,0))
	#end_def

	def verificar_user_senha(self, user_input, senha_input, erro_label, window):
		usuario: str = user_input.get("1.0", "end-1c")
		senha: str = senha_input.get("1.0", "end-1c")

		if len(usuario) == 0 or len(senha) == 0:
			erro_label.config(text="Digite tanto o usuário quanto a senha.", foreground="red")
			return

		self.db_manager = DatabaseManager(
			host="localhost",
			user=usuario,
			password=senha,
			database="publicacao"
		)

		try:
			self.db_manager.connect()
			window.destroy()
		except:
			erro_label.config(text="Digite um usuário ou senha válidos.", foreground="red")
	#end_def

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
	#end_def

	def inserir_titulo(self):
		window = self.graphics_manager.create_window("Inserir Título", "400x300", False)
		window.grid_rowconfigure(0, weight=1)
		window.grid_columnconfigure(0, weight=1)

		main_frame = self.graphics_manager.create_frame(window)
		main_frame.pack(fill=tk.BOTH, expand=True)
		main_frame.grid_rowconfigure(4, weight=1)
		main_frame.grid_columnconfigure(0, weight=1)

		id_label = self.graphics_manager.create_label(main_frame, "ID do livro:")
		id_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
		id_input = self.graphics_manager.create_entry(main_frame)
		id_input.grid(row=0, column=1, pady=10, sticky="ew")

		titulo_label = self.graphics_manager.create_label(main_frame, "Título do livro:")
		titulo_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
		titulo_input = self.graphics_manager.create_entry(main_frame)
		titulo_input.grid(row=1, column=1, pady=10, sticky="ew")

		tipo_label = self.graphics_manager.create_label(main_frame, "Tipo de livro:")
		tipo_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
		tipo_input = self.graphics_manager.create_entry(main_frame)
		tipo_input.grid(row=2, column=1, pady=10, sticky="ew")

		data_label = self.graphics_manager.create_label(main_frame, "Data de pub. do livro:")
		data_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
		data_input = self.graphics_manager.create_entry(main_frame)
		data_input.grid(row=3, column=1, pady=10, sticky="ew")

		erro_label = self.graphics_manager.create_label(main_frame, "", font=('Arial', 12))
		erro_label.config(foreground="red", wraplength=350, justify="left", anchor="w")
		erro_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

		botoes_frame = self.graphics_manager.create_frame(main_frame, padding=0)
		botoes_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="se")
		ok_button = ttk.Button(
			botoes_frame,
			text="Ok",
			command=lambda: self.handle_inserir_titulo(
				id_input,
				titulo_input,
				tipo_input,
				data_input,
				erro_label,
				window
			)
		)
		ok_button.pack(side=tk.RIGHT, padx=(5,0))
		cancelar_button = ttk.Button(botoes_frame, text="Cancelar", command=window.destroy)
		cancelar_button.pack(side=tk.RIGHT, padx=(0,5))
	#end_def
	def handle_inserir_titulo(self, id_input, titulo_input, tipo_input, data_input, erro_label, window):
		ID = id_input.get("1.0", "end-1c").strip()
		TITULO = titulo_input.get("1.0", "end-1c").strip()
		TIPO = tipo_input.get("1.0", "end-1c").strip()
		DATA = data_input.get("1.0", "end-1c").strip()

		if not ID or not TITULO or not TIPO or not DATA:
			erro_label.config(text="Dados inválidos: um ou mais campos estão vazios.")
			return
		elif not self.verificar_formatacao_data(DATA):
			erro_label.config(text="Verifique se a formatação da data está correta: yyyy-mm-dd, yyyy mm dd ou yyyy/mm/dd.\nOu então verifique se digitou ano, mês ou dia válido.")
			return
		
		data_formatted = DATA.replace(' ', '-').replace('/', '-')

		if self.db_manager.inserir_publicacao(ID, TITULO, TIPO, data_formatted):
			erro_label.config(text="Publicação inserida com sucesso!", foreground="green")
		else:
			erro_label.config(text="Erro ao inserir publicação: ID já existe no banco de dados.")
	#end_def

	def alterar_titulo(self):
		window = self.graphics_manager.create_window("Alterar Título", "400x300", False)
		window.grid_rowconfigure(0, weight=1)
		window.grid_columnconfigure(0, weight=1)

		main_frame = self.graphics_manager.create_frame(window)
		main_frame.pack(fill=tk.BOTH, expand=True)
		main_frame.grid_rowconfigure(4, weight=1)
		main_frame.grid_columnconfigure(0, weight=1)

		id_label = self.graphics_manager.create_label(main_frame, "ID do livro*:")
		id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
		id_input = self.graphics_manager.create_entry(main_frame)
		id_input.grid(row=0, column=1, pady=10, sticky="ew")

		titulo_label = self.graphics_manager.create_label(main_frame, "Título do livro:")
		titulo_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
		titulo_input = self.graphics_manager.create_entry(main_frame)
		titulo_input.grid(row=1, column=1, pady=10, sticky="ew")

		tipo_label = self.graphics_manager.create_label(main_frame, "Tipo de livro:")
		tipo_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
		tipo_input = self.graphics_manager.create_entry(main_frame)
		tipo_input.grid(row=2, column=1, pady=10, sticky="ew")

		data_label = self.graphics_manager.create_label(main_frame, "Data de pub. do livro:")
		data_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
		data_input = self.graphics_manager.create_entry(main_frame)
		data_input.grid(row=3, column=1, pady=10, sticky="ew")

		erro_label = self.graphics_manager.create_label(main_frame, "", font=('Arial', 12))
		erro_label.config(foreground="red", wraplength=350, justify="left", anchor="w")
		erro_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

		botoes_frame = self.graphics_manager.create_frame(main_frame, padding=0)
		botoes_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="se")
		ok_button = ttk.Button(
			botoes_frame,
			text="Ok",
			command=lambda: self.handle_alterar_titulo(
				id_input,
				titulo_input,
				tipo_input,
				data_input,
				erro_label,
				window
			)
		)
		ok_button.pack(side=tk.RIGHT, padx=(5,0))
		cancelar_button = ttk.Button(botoes_frame, text="Cancelar", command=window.destroy)
		cancelar_button.pack(side=tk.RIGHT, padx=(0,5))
	#end_def
	def handle_alterar_titulo(self, id_input, titulo_input, tipo_input, data_input, erro_label, window):
		ID = id_input.get("1.0", "end-1c").strip()
		TITULO = titulo_input.get("1.0", "end-1c").strip()
		TIPO = tipo_input.get("1.0", "end-1c").strip()
		DATA = data_input.get("1.0", "end-1c").strip()

		if not ID:
			erro_label.config(text="Digite o ID do livro que deseja alterar.")
			return
		elif not TITULO and not TIPO and not DATA:
			erro_label.config(text="Dados inválidos: todos os campos estão vazios")
			return
		elif DATA and not self.verificar_formatacao_data(DATA):
			erro_label.config(text="Verifique se a formatação da data está correta: yyyy-mm-dd, yyyy mm dd ou yyyy/mm/dd.\nOu então verifique se digitou ano, mês ou dia válido.")
			return
		
		data_formatted = DATA.replace(' ', '-').replace('/', '-')

		if self.db_manager.alterar_publicacao(ID, TITULO, TIPO, data_formatted):
			erro_label.config(text="Publicação alterada com sucesso!", foreground="green")
		else:
			erro_label.config(text="Erro ao alterar publicação: verifique se o ID existe no banco de dados.")
	#end_def

	def excluir_titulo(self): 
		window = self.graphics_manager.create_window("Excluir Título", "400x300", False)
		window.grid_rowconfigure(0, weight=1)
		window.grid_columnconfigure(0, weight=1)

		main_frame = self.graphics_manager.create_frame(window)
		main_frame.pack(fill=tk.BOTH, expand=True)
		main_frame.grid_rowconfigure(4, weight=1)
		main_frame.grid_columnconfigure(0, weight=1)

		id_label = self.graphics_manager.create_label(main_frame, "ID do livro:")
		id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
		id_input = self.graphics_manager.create_entry(main_frame)
		id_input.grid(row=0, column=1, pady=10, sticky="w")

		titulo_label = self.graphics_manager.create_label(main_frame, "Título do livro:")
		titulo_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
		titulo_input = self.graphics_manager.create_entry(main_frame)
		titulo_input.grid(row=1, column=1, pady=10, sticky="w")

		radio_frame = self.graphics_manager.create_frame(main_frame, padding=0)
		radio_label = self.graphics_manager.create_label(radio_frame, "Escolha o critério de exclusão:")
		radio_label.pack(side=tk.LEFT, padx=(0,10))
		radio_var = tk.StringVar(value="deletar_via")
		radio_values = [("Deletar via ID", "id"), ("Deletar via Título", "titulo")]
		for text, value in radio_values:
			radio_button = ttk.Radiobutton(radio_frame, text=text, variable=radio_var, value=value)
			radio_button.pack(side=tk.LEFT)
		#end_for
		radio_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

		erro_label = self.graphics_manager.create_label(main_frame, "", font=('Arial', 12))
		erro_label.config(foreground="red", wraplength=350, justify="left", anchor="w")
		erro_label.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

		botoes_frame = self.graphics_manager.create_frame(main_frame, padding=0)
		botoes_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="se")
		ok_button = ttk.Button(
			botoes_frame,
			text="Ok",
			command=lambda: self.handle_excluir_titulo(
				id_input,
				titulo_input,
				radio_var,
				erro_label
			)
		)
		ok_button.pack(side=tk.RIGHT, padx=(5,0))
		cancelar_button = ttk.Button(botoes_frame, text="Cancelar", command=window.destroy)
		cancelar_button.pack(side=tk.RIGHT, padx=(0,5))
	#end_def
	def handle_excluir_titulo(self, id_input, titulo_input, radio_var, erro_label):
		ID = id_input.get("1.0", "end-1c").strip()
		TITULO = titulo_input.get("1.0", "end-1c").strip()
		CRITERIO = radio_var.get()

		if CRITERIO == "id" and not ID:
			erro_label.config(text="Digite o ID do livro que deseja excluir.")
			return
		elif CRITERIO == "titulo" and not TITULO:
			erro_label.config(text="Digite o Título do livro que deseja excluir.")
			return

		PELO_ID = CRITERIO == "id"

		if self.db_manager.deletar_publicacao(ID, TITULO, PELO_ID):
			erro_label.config(text="Publicação excluída com sucesso!", foreground="green")
		else:
			erro_label.config(text="Erro ao excluir publicação: verifique se o ID/Título existe no banco de dados.")
	#end_def

	def consultar_titulos(self):
		window = self.graphics_manager.create_window("Consultar Títulos", "2000x500", True)
		main_frame = self.graphics_manager.create_frame(window)
		main_frame.pack(fill=tk.BOTH, expand=True)

		results = self.db_manager.consultar_todas_publicacoes()
		if not results:
			no_data_label = self.graphics_manager.create_label(main_frame, "Nenhuma publicação encontrada no banco de dados.")
			no_data_label.pack(pady=5)
			return
		#end_if

		column_names = [i[0] for i in self.db_manager.execute_query("SHOW COLUMNS FROM titulos")]
		tree = ttk.Treeview(main_frame, columns=column_names, show='headings')
		for col in column_names:
			tree.heading(col, text=col)
			tree.column(col, width=150)
		for row in results:
			tree.insert('', tk.END, values=row)
		tree.pack(fill=tk.BOTH, expand=True)

		window.geometry(f"{min(2000, (len(column_names) * 150) + 50)}x500")
	#end_def
		
	def consultar_titulo_criterio(self):
		resultado: list = []

		window = self.graphics_manager.create_window("Consultar Títulos", "2000x500", True)
		main_frame = self.graphics_manager.create_frame(window)
		main_frame.pack(fill=tk.BOTH, expand=True)

		id_label = self.graphics_manager.create_label(main_frame, "ID do livro:")
		id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
		id_input = self.graphics_manager.create_entry(main_frame)
		id_input.grid(row=0, column=1, pady=10, sticky="w")

		titulo_label = self.graphics_manager.create_label(main_frame, "Título do livro:")
		titulo_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
		titulo_input = self.graphics_manager.create_entry(main_frame)
		titulo_input.grid(row=1, column=1, columnspan=4, pady=10, sticky="w")

		data_frame = self.graphics_manager.create_frame(main_frame)
		data_frame.grid(row=2, column=0, columnspan=4)

		data_label = self.graphics_manager.create_label(data_frame, "Data de publicação: entre")
		data_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

		data_antes_input = self.graphics_manager.create_entry(data_frame)
		data_antes_input.grid(row=0, column=1, pady=10, sticky="w")
		
		e_label = self.graphics_manager.create_label(data_frame, "e")
		e_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

		data_depois_input = self.graphics_manager.create_entry(data_frame)
		data_depois_input.grid(row=0, column=3, pady=10, sticky="w")

		erro_label = self.graphics_manager.create_label(main_frame, "")
		erro_label.config(foreground="red")
		erro_label.grid(row=3, column=0, columnspan=4)

		botao = self.graphics_manager.create_button(main_frame, "Consultar", command=lambda: self.handle_consultar_titulo_criterio(id_input, titulo_input, data_antes_input, data_depois_input, erro_label, resultado, tree))
		botao.grid(row=4, column=0)

		column_names = [i[0] for i in self.db_manager.execute_query("SHOW COLUMNS FROM titulos")]
		tree = ttk.Treeview(main_frame, columns=column_names, show='headings')
		tree.grid(row=5, column=0, columnspan=4)

		for col in column_names:
			tree.heading(col, text=col)
			tree.column(col, width=150)

		window.geometry(f"{min(2000, (len(column_names) * 150) + 50)}x500")
	def handle_consultar_titulo_criterio(self, id_input, nome_input, data_antes_input, data_depois_input, erro_label, resultado, tree):
		ID: str = id_input.get("1.0", "end-1c").strip()
		NOME: str = nome_input.get("1.0", "end-1c").strip()
		DATA_ANTES: list = data_antes_input.get("1.0", "end-1c").strip()
		DATA_DEPOIS: list = data_depois_input.get("1.0", "end-1c").strip()

		if not ID and not NOME and not DATA_ANTES and not DATA_DEPOIS:
			erro_label.config(text="Todos os campos estão vazios.")
			return
		elif DATA_ANTES and DATA_DEPOIS and (self.verificar_formatacao_data(data_antes_input) and self.verificar_formatacao_data(data_depois_input)):
			erro_label.config(text="Verifique se a formatação da data está correta: yyyy-mm-dd, yyyy mm dd ou yyyy/mm/dd.\nOu então verifique se digitou ano, mês ou dia válido.")
			return
		
		data_antes_formatada: str = DATA_ANTES.replace(' ', '-').replace('/', '-')
		data_depois_formatada: str = DATA_DEPOIS.replace(' ', '-').replace('/', '-')

		criterio: list = [ID, NOME, [data_antes_formatada, data_depois_formatada]]

		resultado = self.db_manager.consultar_por_criterio(criterio)

		if not resultado:
			erro_label.config(text="Nenhuma publicação encontrada no banco de dados.")
			return
		
		for row in resultado:
			tree.insert('', tk.END, values=row)
	#end_def

	def mostrar_ajuda(self): pass
	def mostrar_licenca(self): pass
	def mostrar_sobre(self): pass
#end_class

class DeprecatedApplication:
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
			command=lambda: ConsultarDados(self.root)
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

class ConsultarDados:
	def __init__(self, parent):
		self.window = tk.Toplevel(parent)
		self.window.title("Consultar publicações")
		self.window.geometry("1000x750")

		main_frame = ttk.Frame(self.window, padding="10")
		main_frame.pack(fill=tk.BOTH, expand=True)

		db = mysql.connector.connect(
            host="localhost",
            user="root",
           	password="serra",
           	database="publicacao"
		)

		cursor = db.cursor()

		cursor.execute("SELECT * FROM titulos")

		columns = ("ID_TITULO", "TITULO_LIVRO", "TIPO_LIVRO",
           	"ID_EDITORA", "PRECO", "TOTAL_VENDA",
			"ROYALTY", "MEDIA_QUANT_VENDAS", "OBSERVACOES", "DATA_PUBLICACAO")
		
		tree = ttk.Treeview(main_frame, columns=columns, show="headings")

		for col in columns:
			tree.heading(col, text=col)
			tree.column(col, width=10, anchor="center")

		for row in cursor.fetchall():
			tree.insert("", "end", values=row)

		tree.pack(fill="both", expand=True)
