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
from tkinter import ttk, messagebox

class DatabaseManager:
	def __init__(self, host: str, user: str, password: str, database: str):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.connection = None

		try:
			import mysql.connector
		except ModuleNotFoundError:
			messagebox.showerror(
				"Não foi possível encontrar dependência",
				"""É necessário ter o mysql-connector instalado em sua máquina para utilizar esse programa.\n
Utilize os seguintes comandos para instala-lo, a dependender do seu sistema operacional:
    Windows: pip install mysql-connector-python
    Linux: pip3 install mysql-connector-python""")
			from sys import exit
			exit(1)
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

	def inserir_publicacao(self, params: dict) -> bool:
		campos: list = []
		valores: list = []
		placeholder: list = []

		for (campo, valor) in params.items():
			if valor:
				campos.append(campo)
				valores.append(valor)
				placeholder.append("%s")

		query = f"INSERT INTO titulos ({','.join(campos)}) VALUES ({','.join(placeholder)})"
		check_query = "SELECT * FROM titulos WHERE ID_TITULO = %s"

		if not self.execute_query(check_query, (params["ID_TITULO"], )):
			self.execute_query(query, tuple(valores))
			return True
		else:
			return False
	#end_def

	def alterar_publicacao(self, params: dict, id: str) -> bool:
		alteracao: list = []
		valores: list = []

		for (campo, valor) in params.items():
			if valor:
				alteracao.append(f"{campo} = %s")
				valores.append(valor)

		if not alteracao:
			return False

		query = f"UPDATE titulos SET {', '.join(alteracao)} WHERE ID_TITULO = " + id
		check_query = "SELECT * FROM titulos WHERE ID_TITULO = " + id

		if self.execute_query(check_query):
			self.execute_query(query, tuple(valores))
			return True
		else:
			return False
	#end_def

	def deletar_publicacao(self, informacao: str, pelo_id: bool) -> bool:
		self.execute_query("SET FOREIGN_KEY_CHECKS = 0")
		where_clause = f"ID_TITULO = '{informacao.strip()}'" if pelo_id else f"TITULO_LIVRO = {informacao.strip()}'"
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
		root.iconphoto(True, tk.PhotoImage(file='res/icon.png'))

		import platform
		if platform.system() == 'Windows':
			root.state("zoomed")
		else:
			root.attributes('-zoomed', True)
		
		self.root.tk.call('source', 'res/forest-light.tcl')
		style = ttk.Style()
		style.configure('.', font=('Segoe UI', 16), background='#f0f0f0')
		style.configure('Treeview', font=('Segoe UI', 10))

		self.setup_navbar()
		self.setup_main_screen()
		self.status = {
			'user': 'Conectado',
			'database': 'publicacao'
		}
		self.statusbar = self.setup_statusbar()
	#end_def

	def setup_navbar(self):
		menubar = tk.Menu(self.root)
		self.root.config(menu=menubar)
		
		arq_menu = tk.Menu(menubar, tearoff=0)
		menubar.add_cascade(label="Arquivo", menu=arq_menu)
		arq_menu.add_command(label="Conectar ao banco de dados", command=self.main_app.conectar_banco)
		arq_menu.add_separator()
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

	def setup_main_screen(self):
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
			font=('Segoe UI', 12),
			text="Sistema de gerenciamento de banco de dados de livros",
		)
		title_label.pack()
		subtitle.pack(pady=(0, 50))

		self.setup_content(main_frame)

		footer_label = ttk.Label(
			main_frame,
			text="COPYLEFT 2025 ASMbleia • Desenvolvido por Ian, João, Rafael, Vitor • Serra, Brasil",
		)
		footer_label.pack(side=tk.BOTTOM, pady=10)
	#end_def

	def setup_content(self, parent: ttk.Frame):
		content_frame = ttk.Frame(parent)
		content_frame.place(anchor=tk.CENTER, relx=0.5, rely=0.5)
		
		left_frame = ttk.LabelFrame(
			content_frame,
			text="Sobre o Programa",
			padding="15",
			labelanchor='n'
		)
		left_frame.grid(row=0, column=0, sticky="nsew", padx=50)
		info_text = """Este sistema oferece um controle completo sobre seu acervo de publicações, permitindo:\n
• Cadastro detalhado de títulos com ID único
• Classificação por tipo de publicação
• Controle de datas de lançamento
• Consultas flexíveis por múltiplos critérios
• Gerenciamento seguro de dados\n
Desenvolvido para atender às necessidades de editoras, bibliotecas e profissionais da área editorial, o sistema garante organização, segurança e eficiência no gerenciamento de publicações."""
		info_label = ttk.Label(
			left_frame,
			text=info_text,
			font=('Segoe UI', 10),
			justify=tk.LEFT,
			wraplength=350
		)
		info_label.pack(anchor=tk.W)
		
		right_frame = ttk.Frame(content_frame)
		right_frame.grid(row=0, column=1, sticky="nsew", pady=(20,0))
		
		actions = [
			("🔐 Conectar ao Banco", self.main_app.conectar_banco),
			("➕ Inserir Título", self.main_app.inserir_titulo),
			("✏️ Alterar Título", self.main_app.alterar_titulo),
			("🗑️ Excluir Título", self.main_app.excluir_titulo),
			("🔍 Consultar Todos os Títulos", self.main_app.consultar_titulos),
			("📊 Consultar por Critério", self.main_app.consultar_titulo_criterio)
		]
		
		for text, command in actions:
			action_label = ttk.Label(
				right_frame,
				text=text,
				font=('Segoe UI', 11),
				cursor="hand2",
				padding="8"
			)
			action_label.pack(anchor=tk.W, fill=tk.X, pady=1)
			
			def on_enter(event, label=action_label):
				label.config(foreground="#217346")
			def on_leave(event, label=action_label):
				label.config(foreground="#333333")
			def on_click(event, func=command):
				func()
			action_label.bind("<Enter>", on_enter)
			action_label.bind("<Leave>", on_leave)
			action_label.bind("<Button-1>", on_click)
	#end_def

	def setup_statusbar(self):
		statusbar = ttk.Label(
			self.root,
			text=f"  Usuário: {self.status['user']} | Banco de Dados: {self.status['database']}",
			relief=tk.SUNKEN,
			anchor=tk.W,
			font=('Segoe UI', 12),
			background="#f0f0f0"
		)
		statusbar.pack(side=tk.BOTTOM, fill=tk.X, ipady=2)
		return statusbar
	#end_def

	def create_window(self, title: str, size: str = "400x300", resizable: bool = False) -> tk.Toplevel:
		window = tk.Toplevel(self.root)
		window.title(title)
		window.geometry(size)

		# Não entendi direito, mas isso permite centralizar a janela
		window.update_idletasks()
		
		width, height = map(int, size.split('x'))
		x = (window.winfo_screenwidth() - width) // 2
		y = (window.winfo_screenheight() - height) // 2
		window.geometry(f"{width}x{height}+{x}+{y}")
		
		if not resizable:
			window.resizable(False, False)

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
	def __init__(self):
		self.root = tk.Tk()

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

	def conectar_banco(self):
		messagebox.showerror("Conectar ao Banco", "Ainda não implementado")
	#end_def

	def inserir_titulo(self):
		window = self.graphics_manager.create_window("Inserir Título", "400x600", False)
		window.grid_rowconfigure(0, weight=1)
		window.grid_columnconfigure(0, weight=1)

		main_frame = self.graphics_manager.create_frame(window)
		main_frame.pack(fill=tk.BOTH, expand=True)
		main_frame.grid_rowconfigure(10, weight=1)
		main_frame.grid_columnconfigure(0, weight=1)

		id_label = self.graphics_manager.create_label(main_frame, "ID do livro*:")
		id_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
		id_input = self.graphics_manager.create_entry(main_frame)
		id_input.grid(row=0, column=1, pady=10, sticky="ew")

		titulo_label = self.graphics_manager.create_label(main_frame, "Título do livro*:")
		titulo_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
		titulo_input = self.graphics_manager.create_entry(main_frame)
		titulo_input.grid(row=1, column=1, pady=10, sticky="ew")

		tipo_label = self.graphics_manager.create_label(main_frame, "Tipo de livro*:")
		tipo_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
		tipo_input = self.graphics_manager.create_entry(main_frame)
		tipo_input.grid(row=2, column=1, pady=10, sticky="ew")

		data_label = self.graphics_manager.create_label(main_frame, "Data de pub. do livro*:")
		data_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
		data_input = self.graphics_manager.create_entry(main_frame)
		data_input.grid(row=3, column=1, pady=10, sticky="ew")

		id_ed_label = self.graphics_manager.create_label(main_frame, "ID da editora:")
		id_ed_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
		id_ed_input = self.graphics_manager.create_entry(main_frame)
		id_ed_input.grid(row=4, column=1, pady=10, sticky="ew")

		preco_label = self.graphics_manager.create_label(main_frame, "Preço do livro:")
		preco_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
		preco_input = self.graphics_manager.create_entry(main_frame)
		preco_input.grid(row=5, column=1, pady=10, sticky="ew")

		total_venda_label = self.graphics_manager.create_label(main_frame, "Total da venda:")
		total_venda_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
		total_venda_input = self.graphics_manager.create_entry(main_frame)
		total_venda_input.grid(row=6, column=1, pady=10, sticky="ew")

		royalty_label = self.graphics_manager.create_label(main_frame, "Royalty:")
		royalty_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
		royalty_input = self.graphics_manager.create_entry(main_frame)
		royalty_input.grid(row=7, column=1, pady=10, sticky="ew")

		med_qtd_vendas_label = self.graphics_manager.create_label(main_frame, "Média da qtd de vendas:")
		med_qtd_vendas_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")
		med_qtd_vendas_input = self.graphics_manager.create_entry(main_frame)
		med_qtd_vendas_input.grid(row=8, column=1, pady=10, sticky="ew")

		observacoes_label = self.graphics_manager.create_label(main_frame, "Observações:")
		observacoes_label.grid(row=9, column=0, padx=10, pady=10, sticky="w")
		observacoes_input = self.graphics_manager.create_entry(main_frame)
		observacoes_input.grid(row=9, column=1, pady=10, sticky="ew")

		erro_label = self.graphics_manager.create_label(main_frame, "", font=('Arial', 12))
		erro_label.config(foreground="red", wraplength=350, justify="left", anchor="w")
		erro_label.grid(row=10, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

		botoes_frame = self.graphics_manager.create_frame(main_frame, padding=0)
		botoes_frame.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky="se")
		ok_button = ttk.Button(
			botoes_frame,
			text="Ok",
			command=lambda: self.handle_inserir_titulo(
				id_input,
				titulo_input,
				tipo_input,
				data_input,
				id_ed_input,
				preco_input,
				total_venda_input,
				royalty_input,
				med_qtd_vendas_input,
				observacoes_input,
				erro_label,
				window
			)
		)
		ok_button.pack(side=tk.RIGHT, padx=(5,0))
		cancelar_button = ttk.Button(botoes_frame, text="Cancelar", command=window.destroy)
		cancelar_button.pack(side=tk.RIGHT, padx=(0,5))
	#end_def
	def handle_inserir_titulo(self, id_input, titulo_input, tipo_input, data_input, id_ed_input, preco_input, total_venda_input, royalty_input, med_qtd_vendas_input, observacoes_input, erro_label, window):
		ID = id_input.get("1.0", "end-1c").strip()
		TITULO = titulo_input.get("1.0", "end-1c").strip()
		TIPO = tipo_input.get("1.0", "end-1c").strip()
		DATA = data_input.get("1.0", "end-1c").strip()
		ID_ED = id_ed_input.get("1.0", "end-1c").strip()
		PRECO = preco_input.get("1.0", "end-1c").strip()
		TOTAL_VENDA = total_venda_input.get("1.0", "end-1c").strip()
		ROYALTY = royalty_input.get("1.0", "end-1c").strip()
		MED_QTD_VENDAS = med_qtd_vendas_input.get("1.0", "end-1c").strip()
		OBSERVACOES = observacoes_input.get("1.0", "end-1c").strip()

		if not ID and not TITULO and not TIPO and not DATA and not ID_ED and not PRECO and not TOTAL_VENDA and not ROYALTY and not MED_QTD_VENDAS and not OBSERVACOES:
			erro_label.config(text="Dados inválidos: todos os campos estão vazios.")
			return
		elif not ID or not TITULO or not TIPO or not DATA:
			erro_label.config(text="Dados inválidos: há campos obrigatórios vazios.")
			return
		elif not self.verificar_formatacao_data(DATA):
			erro_label.config(text="Verifique se a formatação da data está correta: yyyy-mm-dd, yyyy mm dd ou yyyy/mm/dd.\nOu então verifique se digitou ano, mês ou dia válido.")
			return
		
		data_formatted = DATA.replace(' ', '-').replace('/', '-')

		if self.db_manager.inserir_publicacao({
				"ID_TITULO" : ID,
				"TITULO_LIVRO" : TITULO,
				"TIPO_LIVRO" : TIPO,
				"DATA_PUBLICACAO" : data_formatted,
				"ID_EDITORA" : ID_ED,
				"PRECO" : PRECO,
				"TOTAL_VENDA" : TOTAL_VENDA,
				"ROYALTY" : ROYALTY,
				"MEDIA_QUANT_VENDAS" : MED_QTD_VENDAS,
				"OBSERVACOES" : OBSERVACOES
			}):
			erro_label.config(text="Publicação inserida com sucesso!", foreground="green")
			id_input.delete("1.0", tk.END)
			titulo_input.delete("1.0", tk.END)
			tipo_input.delete("1.0", tk.END)
			data_input.delete("1.0", tk.END)
			id_ed_input.delete("1.0", tk.END)
			preco_input.delete("1.0", tk.END)
			total_venda_input.delete("1.0", tk.END)
			royalty_input.delete("1.0", tk.END)
			med_qtd_vendas_input.delete("1.0", tk.END)
			observacoes_input.delete("1.0", tk.END)
		else:
			erro_label.config(text="Erro ao inserir publicação: ID já existe no banco de dados.")
	#end_def

	def alterar_titulo(self):
		window = self.graphics_manager.create_window("Alterar Título", "400x600", False)
		window.grid_rowconfigure(0, weight=1)
		window.grid_columnconfigure(0, weight=1)

		main_frame = self.graphics_manager.create_frame(window)
		main_frame.pack(fill=tk.BOTH, expand=True)
		main_frame.grid_rowconfigure(10, weight=1)
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


		id_ed_label = self.graphics_manager.create_label(main_frame, "ID da editora:")
		id_ed_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
		id_ed_input = self.graphics_manager.create_entry(main_frame)
		id_ed_input.grid(row=4, column=1, pady=10, sticky="ew")

		preco_label = self.graphics_manager.create_label(main_frame, "Preço do livro:")
		preco_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
		preco_input = self.graphics_manager.create_entry(main_frame)
		preco_input.grid(row=5, column=1, pady=10, sticky="ew")

		total_venda_label = self.graphics_manager.create_label(main_frame, "Total da venda:")
		total_venda_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
		total_venda_input = self.graphics_manager.create_entry(main_frame)
		total_venda_input.grid(row=6, column=1, pady=10, sticky="ew")

		royalty_label = self.graphics_manager.create_label(main_frame, "Royalty:")
		royalty_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
		royalty_input = self.graphics_manager.create_entry(main_frame)
		royalty_input.grid(row=7, column=1, pady=10, sticky="ew")

		med_qtd_vendas_label = self.graphics_manager.create_label(main_frame, "Média da qtd de vendas:")
		med_qtd_vendas_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")
		med_qtd_vendas_input = self.graphics_manager.create_entry(main_frame)
		med_qtd_vendas_input.grid(row=8, column=1, pady=10, sticky="ew")

		observacoes_label = self.graphics_manager.create_label(main_frame, "Observações:")
		observacoes_label.grid(row=9, column=0, padx=10, pady=10, sticky="w")
		observacoes_input = self.graphics_manager.create_entry(main_frame)
		observacoes_input.grid(row=9, column=1, pady=10, sticky="ew")

		erro_label = self.graphics_manager.create_label(main_frame, "", font=('Arial', 12))
		erro_label.config(foreground="red", wraplength=350, justify="left", anchor="w")
		erro_label.grid(row=10, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

		botoes_frame = self.graphics_manager.create_frame(main_frame, padding=0)
		botoes_frame.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky="se")
		ok_button = ttk.Button(
			botoes_frame,
			text="Ok",
			command=lambda: self.handle_alterar_titulo(
				id_input,
				titulo_input,
				tipo_input,
				data_input,
				id_ed_input,
				preco_input,
				total_venda_input,
				royalty_input,
				med_qtd_vendas_input,
				observacoes_input,
				erro_label,
				window
			)
		)
		ok_button.pack(side=tk.RIGHT, padx=(5,0))
		cancelar_button = ttk.Button(botoes_frame, text="Cancelar", command=window.destroy)
		cancelar_button.pack(side=tk.RIGHT, padx=(0,5))
	#end_def
	def handle_alterar_titulo(self, id_input, titulo_input, tipo_input, data_input, id_ed_input, preco_input, total_venda_input, royalty_input, med_qtd_vendas_input, observacoes_input, erro_label, window):
		ID = id_input.get("1.0", "end-1c").strip()
		TITULO = titulo_input.get("1.0", "end-1c").strip()
		TIPO = tipo_input.get("1.0", "end-1c").strip()
		DATA = data_input.get("1.0", "end-1c").strip()
		ID_ED = id_ed_input.get("1.0", "end-1c").strip()
		PRECO = preco_input.get("1.0", "end-1c").strip()
		TOTAL_VENDA = total_venda_input.get("1.0", "end-1c").strip()
		ROYALTY = royalty_input.get("1.0", "end-1c").strip()
		MED_QTD_VENDAS = med_qtd_vendas_input.get("1.0", "end-1c").strip()
		OBSERVACOES = observacoes_input.get("1.0", "end-1c").strip()

		if not ID and not TITULO and not TIPO and not DATA and not ID_ED and not PRECO and not TOTAL_VENDA and not ROYALTY and not MED_QTD_VENDAS and not OBSERVACOES:
			erro_label.config(text="Dados inválidos: todos os campos estão vazios.")
			return
		elif not ID:
			erro_label.config(text="Digite o ID do livro que deseja alterar.")
			return
		elif DATA and not self.verificar_formatacao_data(DATA):
			erro_label.config(text="Verifique se a formatação da data está correta: yyyy-mm-dd, yyyy mm dd ou yyyy/mm/dd.\nOu então verifique se digitou ano, mês ou dia válido.")
			return
		
		data_formatted = DATA.replace(' ', '-').replace('/', '-')

		if self.db_manager.alterar_publicacao({
			"TITULO_LIVRO" : TITULO,
			"TIPO_LIVRO" : TIPO,
			"DATA_PUBLICACAO" : data_formatted,
			"ID_EDITORA" : ID_ED,
			"PRECO" : PRECO,
			"TOTAL_VENDA" : TOTAL_VENDA,
			"ROYALTY" : ROYALTY,
			"MEDIA_QUANT_VENDAS" : MED_QTD_VENDAS,
			"OBSERVACOES" : OBSERVACOES
		}, ID):
			erro_label.config(text="Publicação alterada com sucesso!", foreground="green")
			id_input.delete("1.0", tk.END)
			titulo_input.delete("1.0", tk.END)
			tipo_input.delete("1.0", tk.END)
			data_input.delete("1.0", tk.END)
			id_ed_input.delete("1.0", tk.END)
			preco_input.delete("1.0", tk.END)
			total_venda_input.delete("1.0", tk.END)
			royalty_input.delete("1.0", tk.END)
			med_qtd_vendas_input.delete("1.0", tk.END)
			observacoes_input.delete("1.0", tk.END)
		else:
			erro_label.config(text="Erro ao alterar publicação: verifique se o ID existe no banco de dados.", foreground="red")
	#end_def

	def excluir_titulo(self): 
		window = self.graphics_manager.create_window("Excluir Título", "400x300", False)
		window.grid_rowconfigure(0, weight=1)
		window.grid_columnconfigure(0, weight=1)

		main_frame = self.graphics_manager.create_frame(window)
		main_frame.pack(fill=tk.BOTH, expand=True)
		main_frame.grid_rowconfigure(4, weight=1)
		main_frame.grid_columnconfigure(0, weight=1)

		informacao_label = self.graphics_manager.create_label(main_frame, "Informação do livro:")
		informacao_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")
		informacao_input = self.graphics_manager.create_entry(main_frame)
		informacao_input.grid(row=0, column=1, pady=10, sticky="w")

		radio_label = self.graphics_manager.create_label(main_frame, "Escolha o critério de exclusão:")
		radio_label.grid(row=1, column=0, padx=(0, 10), pady=10, columnspan=2, sticky="ws")
		radio_frame = self.graphics_manager.create_frame(main_frame, padding=0)
		radio_var = tk.StringVar(value="deletar_via")
		radio_values = [("Deletar via ID", "id"), ("Deletar via Título", "titulo")]
		for text, value in radio_values:
			radio_button = ttk.Radiobutton(radio_frame, text=text, variable=radio_var, value=value)
			radio_button.pack(side=tk.RIGHT)
		#end_for
		radio_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ws")

		erro_label = self.graphics_manager.create_label(main_frame, "")
		erro_label.config(foreground="red", wraplength=350, justify="left", anchor="w")
		erro_label.grid(row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

		botoes_frame = self.graphics_manager.create_frame(main_frame, padding=0)
		botoes_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="se")
		ok_button = ttk.Button(
			botoes_frame,
			text="Ok",
			command=lambda: self.handle_excluir_titulo(
				informacao_input,
				radio_var,
				erro_label
			)
		)
		ok_button.pack(side=tk.RIGHT, padx=(5,0))
		cancelar_button = ttk.Button(botoes_frame, text="Cancelar", command=window.destroy)
		cancelar_button.pack(side=tk.RIGHT, padx=(0,5))
	#end_def
	def handle_excluir_titulo(self, informacao_input, radio_var, erro_label):
		INFORMACAO = informacao_input.get("1.0", "end-1c").strip()
		CRITERIO = radio_var.get()

		if CRITERIO == "deletar_via":
			erro_label.config(text="Primeiro, selecione o critério de exclusão.", foreground="red")
			return
		elif INFORMACAO == "":
			erro_label.config(text="Digite um ID/Título antes de excluir!", foreground="red")
			return

		PELO_ID = CRITERIO == "id"

		if self.db_manager.deletar_publicacao(INFORMACAO, PELO_ID):
			erro_label.config(text="Publicação excluída com sucesso!", foreground="green")
			informacao_input.delete("1.0", tk.END)
		else:
			erro_label.config(text="Erro ao excluir publicação: verifique se o ID/Título existe no banco de dados.", foreground="red")
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

		input_frame = self.graphics_manager.create_frame(main_frame, 0)
		input_frame.grid(row=0, column=0, columnspan=4, sticky="w")

		id_label = self.graphics_manager.create_label(input_frame, "ID do livro:")
		id_label.grid(row=0, column=0, sticky="ew")
		id_input = self.graphics_manager.create_entry(input_frame)
		id_input.grid(row=0, column=1, padx=10, sticky="ew")

		titulo_label = self.graphics_manager.create_label(input_frame, "Título do livro:")
		titulo_label.grid(row=1, column=0, pady=10, sticky="ew")
		titulo_input = self.graphics_manager.create_entry(input_frame)
		titulo_input.grid(row=1, column=1, columnspan=3, padx=10, sticky="ew")

		data_frame = self.graphics_manager.create_frame(main_frame, 0)
		data_frame.grid(row=1, column=0, columnspan=4, sticky="w")

		data_label = self.graphics_manager.create_label(data_frame, "Data de publicação: entre")
		data_label.grid(row=0, column=0, sticky="w")

		data_antes_input = self.graphics_manager.create_entry(data_frame)
		data_antes_input.grid(row=0, column=1, padx=(10, 0), sticky="w")
		
		e_label = self.graphics_manager.create_label(data_frame, "e")
		e_label.grid(row=0, column=2, padx=10, sticky="w")

		data_depois_input = self.graphics_manager.create_entry(data_frame)
		data_depois_input.grid(row=0, column=3, sticky="w")

		erro_label = self.graphics_manager.create_label(main_frame, "")
		erro_label.config(foreground="red")
		erro_label.grid(row=2, column=0, columnspan=4)

		botao = self.graphics_manager.create_button(main_frame, "Consultar", command=lambda: self.handle_consultar_titulo_criterio(id_input, titulo_input, data_antes_input, data_depois_input, erro_label, resultado, tree))
		botao.grid(row=3, column=0, sticky="w")

		column_names = [i[0] for i in self.db_manager.execute_query("SHOW COLUMNS FROM titulos")]
		tree = ttk.Treeview(main_frame, columns=column_names, show='headings')
		tree.grid(row=4, column=0, columnspan=4)

		for col in column_names:
			tree.heading(col, text=col)
			tree.column(col, width=150)

		window.geometry(f"{min(2000, (len(column_names) * 150) + 50)}x500")
	#end_def
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
			erro_label.config(text="Nenhuma publicação encontrada no banco de dados.", foreground="red")
			return
		
		for row in resultado:
			tree.insert('', tk.END, values=row)
	#end_def

	def mostrar_ajuda(self):
		messagebox.showinfo("Como usar o Gerenciador", "Também não sabemos, boa sorte!")
	#end_def

	def mostrar_licenca(self):
		license_window = self.graphics_manager.create_window("Licença", "535x500", True)
		
		text_widget = tk.Text(
			license_window,
			wrap=tk.WORD,
			font=('Courier New', 9),
			bg='white'
		)
		scrollbar = ttk.Scrollbar(license_window, command=text_widget.yview)
		text_widget.config(yscrollcommand=scrollbar.set)
		
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		
		with open("LICENSE", "r", encoding="utf-8") as file:
			license_text = file.read()
		
		text_widget.insert("1.0", license_text)
		text_widget.config(state=tk.DISABLED)
	#end_def

	def mostrar_sobre(self):
		about_window = self.graphics_manager.create_window("Sobre a Aplicação", "500x400")
		
		main_frame = ttk.Frame(about_window, padding=20)
		main_frame.pack(fill=tk.BOTH, expand=True)

		icon = tk.PhotoImage(file="res/icon.png").subsample(16)
		icon_label = ttk.Label(main_frame, image=icon)
		icon_label.image = icon
		icon_label.pack(pady=10)

		ttk.Label(
			main_frame,
			text="Gerenciador de Publicações",
			font=('Segoe UI', 16, 'bold')
		).pack()

		ttk.Label(
			main_frame,
			text="Desenvolvido por ASMbleia",
			font=('Segoe UI', 12)
		).pack(pady=10)

		ttk.Label(
			main_frame,
			text="""Ian Caliel Matos Cabral
João Paulo Pipper da Silva
Rafael Cabral Lopes
Vitor Felberg Barcelos""",
			font=('Segoe UI', 11),
			justify=tk.CENTER
		).pack(pady=10)

		ttk.Label(
			main_frame,
			text="Serra, Brasil • 2024",
			font=('Segoe UI', 10, 'italic'),
			foreground="#7F8C8D"
		).pack(pady=20)
	#end_def
#end_class