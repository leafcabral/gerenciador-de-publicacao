"""
ASMbleia
	Ian Caliel Matos Cabral
	João Paulo Pipper da Silva
	Rafael Cabral Lopes
	Vitor Felberg Barcelos
Serra, Brasil
TODO TODO TODO TODO TODO TODO TODO TODO 

Autora original: Alessandra Aguiar Vilarinho 
"""
import tkinter as tk
from tkinter import ttk

import mod

class ChildWindow:
    def __init__(self, parent, title, content):
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.minsize(400, 300)
        self.window.resizable(False, False)

        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=False)
        
        # Conteúdo da janela
        label = ttk.Label(main_frame, text=content, font=('Arial', 12))
        label.pack(pady=20)
        
        # Botão de fechar
        close_button = ttk.Button(
            main_frame, 
            text="Fechar", 
            command=self.window.destroy
        )
        close_button.pack(pady=10)


class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Publicações")
        self.root.geometry("800x600")

        self.root.minsize(800, 600)
        
        # Configurar o menu principal
        self.setup_menu()
        
        # Conteúdo da janela principal
        self.setup_content()
    
    def setup_content(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="vtkaxx", 
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=10)
        
        # Descrição
        desc_label = ttk.Label(
            main_frame, 
            text="leafcabral",
            font=('Arial', 12, 'bold')
        )
        desc_label.pack(pady=20)
        
        # Rodapé
        footer_label = ttk.Label(
            main_frame, 
            text="calielian",
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
            label="Inserir", 
            command=lambda: mod.InserirDados(self.root)
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Alterar", 
            command=lambda: ChildWindow(self.root, "Alterar empregado", "Aqui entra sua janela com\n\n\nlógica para alterar um empregado")
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Excluir", 
            command=lambda: ChildWindow(self.root, "Excluir empregado", "Aqui entra sua janela com\n\n\nlógica para excluir um empregado")
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Consultar por critério", 
            command=lambda: ChildWindow(self.root, "Consultar por critério", "Aqui entra sua janela com\n\n\nlógica para consultar um empregado por um critério")
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Consultar todos", 
            command=lambda: ChildWindow(self.root, "Consultar todos", "Aqui entra sua janela com\n\n\nlógica para consultar todos empregados")
        )
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(
            label="Socorro quero terminar este trabalho...", 
            command=lambda: ChildWindow(self.root, "Terminando as disciplinas de programação com a profa. Alessandra.", "Adeus Programação em Python")
        )
        help_menu.add_separator()
        help_menu.add_command(label="Sobre", command=self.show_about)
    
    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("Sobre")
        about_window.geometry("300x200")
        
        ttk.Label(about_window, text="Gerenciador de Publicações", font=('Arial', 14)).pack(pady=10)
        ttk.Label(about_window, text="Versão 1.0").pack()
        ttk.Label(about_window, text="Desenvolvidos por ASMbleia\nAutora original: Alessandra Aguiar").pack(pady=10)
        
        ttk.Button(about_window, text="OK", command=about_window.destroy).pack(pady=20)

def main() -> None:
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()