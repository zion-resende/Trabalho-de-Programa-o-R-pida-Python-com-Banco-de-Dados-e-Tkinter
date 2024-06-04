import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import datetime

class BancoDeDados:
    def __init__(self):
        self.conexao = sqlite3.connect("tarefas.db")
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            usuario TEXT,
            senha TEXT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY,
            nome TEXT
        )
        """)
        self.conexao.commit()

    def adicionar_usuario(self, usuario, senha):
        self.cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        self.conexao.commit()

    def buscar_usuario(self, usuario, senha):
        self.cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        return self.cursor.fetchone()

    def adicionar_tarefa(self, nome):
        self.cursor.execute("INSERT INTO tarefas (nome) VALUES (?)", (nome,))
        self.conexao.commit()

    def listar_tarefas(self):
        self.cursor.execute("SELECT * FROM tarefas")
        return self.cursor.fetchall()

    def atualizar_tarefa(self, nome_tarefa, novo_nome):
        self.cursor.execute("UPDATE tarefas SET nome = ? WHERE nome = ?", (novo_nome, nome_tarefa))
        self.conexao.commit()

    def excluir_tarefa(self, nome_tarefa):
        self.cursor.execute("DELETE FROM tarefas WHERE nome = ?", (nome_tarefa,))
        self.conexao.commit()

    def fechar_conexao(self):
        self.conexao.close()

class InterfaceGrafica:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciador de Tarefas")
        self.master.geometry("400x400")
        self.master.config(bg="#f0f0f0")
        
        self.banco = BancoDeDados()

        self.carregar_login()

        self.mostrar_opcoes_iniciais()

    def mostrar_opcoes_iniciais(self):
        self.limpar_tela()

        self.frame_inicial = tk.Frame(self.master, bg="#f0f0f0")
        self.frame_inicial.pack(expand=True, fill="both")

        self.botao_login = tk.Button(self.frame_inicial, text="Login", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.mostrar_login)
        self.botao_login.pack(pady=20, ipadx=10, ipady=5)

        self.botao_cadastro = tk.Button(self.frame_inicial, text="Cadastro", font=("Arial", 14), bg="#008CBA", fg="white", command=self.mostrar_cadastro)
        self.botao_cadastro.pack(ipadx=10, ipady=5)

    def mostrar_cadastro(self):
        self.limpar_tela()

        self.frame_cadastro = tk.Frame(self.master, bg="#f0f0f0")
        self.frame_cadastro.pack(expand=True, fill="both")

        self.label_usuario = tk.Label(self.frame_cadastro, text="Novo Usuário:", bg="#f0f0f0", font=("Arial", 14))
        self.label_usuario.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_usuario = tk.Entry(self.frame_cadastro, font=("Arial", 14))
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)

        self.label_senha = tk.Label(self.frame_cadastro, text="Nova Senha:", bg="#f0f0f0", font=("Arial", 14))
        self.label_senha.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_senha = tk.Entry(self.frame_cadastro, show="*", font=("Arial", 14))
        self.entry_senha.grid(row=1, column=1, padx=5, pady=5)

        self.botao_cadastrar = tk.Button(self.frame_cadastro, text="Cadastrar", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.criar_conta)
        self.botao_cadastrar.grid(row=2, columnspan=2, padx=5, pady=20, ipadx=10, ipady=5)

        self.botao_voltar = tk.Button(self.frame_cadastro, text="Voltar", font=("Arial", 14), bg="#f44336", fg="white", command=self.mostrar_opcoes_iniciais)
        self.botao_voltar.grid(row=3, columnspan=2, padx=5, pady=5, ipadx=10, ipady=5)

    def mostrar_login(self):
        self.limpar_tela()

        self.frame_login = tk.Frame(self.master, bg="#f0f0f0")
        self.frame_login.pack(expand=True, fill="both")

        self.label_usuario = tk.Label(self.frame_login, text="Usuário:", bg="#f0f0f0", font=("Arial", 14))
        self.label_usuario.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_usuario = tk.Entry(self.frame_login, font=("Arial", 14))
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)

        self.label_senha = tk.Label(self.frame_login, text="Senha:", bg="#f0f0f0", font=("Arial", 14))
        self.label_senha.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_senha = tk.Entry(self.frame_login, show="*", font=("Arial", 14))
        self.entry_senha.grid(row=1, column=1, padx=5, pady=5)

        self.botao_login = tk.Button(self.frame_login, text="Login", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.fazer_login)
        self.botao_login.grid(row=2, columnspan=2, padx=5, pady=20, ipadx=10, ipady=5)

        self.botao_voltar = tk.Button(self.frame_login, text="Voltar", font=("Arial", 14), bg="#f44336", fg="white", command=self.mostrar_opcoes_iniciais)
        self.botao_voltar.grid(row=3, columnspan=2, padx=5, pady=5, ipadx=10, ipady=5)

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        usuario_info = self.banco.buscar_usuario(usuario, senha)
        if usuario_info:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario}!")
            self.salvar_login(usuario)
            self.mostrar_menu()  # Corrigido: chamar mostrar_menu() após o login
        else:
            messagebox.showerror("Erro de login", "Nome de usuário ou senha incorretos.")

    def criar_conta(self):
        novo_usuario = self.entry_usuario.get()
        nova_senha = self.entry_senha.get()
        if novo_usuario and nova_senha:
            self.banco.adicionar_usuario(novo_usuario, nova_senha)
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            self.mostrar_login()  # Redirecionar
        self.mostrar_login()  # Redirecionar para a tela de login após o cadastro

    def mostrar_menu(self):
        self.limpar_tela()

        self.frame_menu = tk.Frame(self.master, bg="#f0f0f0")
        self.frame_menu.pack(expand=True, fill="both")

        self.label_titulo = tk.Label(self.frame_menu, text="Menu Principal", bg="#f0f0f0", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=10)

        botoes = [
            ("Criar Tarefa", self.mostrar_criar_tarefa),
            ("Atualizar Tarefa", self.mostrar_atualizar_tarefa),
            ("Excluir Tarefa", self.mostrar_excluir_tarefa),
            ("Visualizar Tarefas", self.mostrar_tarefas),
            ("Sair", self.master.quit)
        ]

        for texto, comando in botoes:
            botao = tk.Button(self.frame_menu, text=texto, font=("Arial", 14), bg="#008CBA", fg="white", command=comando)
            botao.pack(pady=5, ipadx=10, ipady=5)

    def mostrar_criar_tarefa(self):
        self.limpar_tela()

        self.frame_criar_tarefa = tk.Frame(self.master, bg="#f0f0f0")
        self.frame_criar_tarefa.pack(expand=True, fill="both")

        self.label_nome_tarefa = tk.Label(self.frame_criar_tarefa, text="Nome da Tarefa:", bg="#f0f0f0", font=("Arial", 14))
        self.label_nome_tarefa.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nome_tarefa = tk.Entry(self.frame_criar_tarefa, font=("Arial", 14))
        self.entry_nome_tarefa.grid(row=0, column=1, padx=5, pady=5)

        self.botao_criar = tk.Button(self.frame_criar_tarefa, text="Criar Tarefa", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.criar_tarefa)
        self.botao_criar.grid(row=1, columnspan=2, padx=5, pady=20, ipadx=10, ipady=5)

        self.botao_voltar = tk.Button(self.frame_criar_tarefa, text="Voltar", font=("Arial", 14), bg="#f44336", fg="white", command=self.mostrar_menu)
        self.botao_voltar.grid(row=2, columnspan=2, padx=5, pady=5, ipadx=10, ipady=5)

    def mostrar_atualizar_tarefa(self):
        self.limpar_tela()

        self.frame_atualizar_tarefa = tk.Frame(self.master, bg="#f0f0f0")
        self.frame_atualizar_tarefa.pack(expand=True, fill="both")

        self.label_nome_tarefa = tk.Label(self.frame_atualizar_tarefa, text="Nome da Tarefa:", bg="#f0f0f0", font=("Arial", 14))
        self.label_nome_tarefa.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nome_tarefa_atualizar = tk.Entry(self.frame_atualizar_tarefa, font=("Arial", 14))
        self.entry_nome_tarefa_atualizar.grid(row=0, column=1, padx=5, pady=5)

        self.label_novo_nome = tk.Label(self.frame_atualizar_tarefa, text="Novo Nome:", bg="#f0f0f0", font=("Arial", 14))
        self.label_novo_nome.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_novo_nome = tk.Entry(self.frame_atualizar_tarefa, font=("Arial", 14))
        self.entry_novo_nome.grid(row=1, column=1, padx=5, pady=5)

        self.botao_atualizar = tk.Button(self.frame_atualizar_tarefa, text="Atualizar", font=("Arial", 14), bg="#008CBA", fg="white", command=self.atualizar_tarefa)
        self.botao_atualizar.grid(row=2, columnspan=2, padx=5, pady=20, ipadx=10, ipady=5)

        self.botao_voltar = tk.Button(self.frame_atualizar_tarefa, text="Voltar", font=("Arial", 14), bg="#f44336", fg="white", command=self.mostrar_menu)
        self.botao_voltar.grid(row=3, columnspan=2, padx=5, pady=5, ipadx=10, ipady=5)

    def mostrar_excluir_tarefa(self):
        self.limpar_tela()

        self.frame_excluir_tarefa = tk.Frame(self.master, bg="#f0f0f0")
        self.frame_excluir_tarefa.pack(expand=True, fill="both")

        self.label_nome_tarefa_excluir = tk.Label(self.frame_excluir_tarefa, text="Nome da Tarefa:", bg="#f0f0f0", font=("Arial", 14))
        self.label_nome_tarefa_excluir.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nome_tarefa_excluir = tk.Entry(self.frame_excluir_tarefa, font=("Arial", 14))
        self.entry_nome_tarefa_excluir.grid(row=0, column=1, padx=5, pady=5)

        self.botao_excluir = tk.Button(self.frame_excluir_tarefa, text="Excluir", font=("Arial", 14), bg="#f44336", fg="white", command=self.excluir_tarefa)
        self.botao_excluir.grid(row=1, columnspan=2, padx=5, pady=20, ipadx=10, ipady=5)

        self.botao_voltar = tk.Button(self.frame_excluir_tarefa, text="Voltar", font=("Arial", 14), bg="#f44336", fg="white", command=self.mostrar_menu)
        self.botao_voltar.grid(row=2, columnspan=2, padx=5, pady=5, ipadx=10, ipady=5)
        self.botao_voltar = tk.Button(self.frame_excluir_tarefa, text="Voltar", font=("Arial", 14), bg="#f44336", fg="white", command=self.mostrar_menu)
        self.botao_voltar.grid(row=2, columnspan=2, padx=5, pady=5, ipadx=10, ipady=5)

    def mostrar_tarefas(self):
        self.limpar_tela()

        tarefas = self.banco.listar_tarefas()
        if not tarefas:
            messagebox.showinfo("Tarefas", "Não há tarefas cadastradas.")
            self.mostrar_menu()
            return

        self.frame_tarefas = tk.Frame(self.master, bg="#f0f0f0")
        self.frame_tarefas.pack(expand=True, fill="both")

        self.label_titulo = tk.Label(self.frame_tarefas, text="Tarefas", bg="#f0f0f0", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=10)

        for index, tarefa in enumerate(tarefas, start=1):
            label_tarefa = tk.Label(self.frame_tarefas, text=f"{index}. {tarefa[1]}", bg="#f0f0f0", font=("Arial", 14))
            label_tarefa.pack(pady=5)

        self.botao_voltar = tk.Button(self.frame_tarefas, text="Voltar", font=("Arial", 14), bg="#f44336", fg="white", command=self.mostrar_menu)
        self.botao_voltar.pack(pady=5, ipadx=10, ipady=5)

    def criar_tarefa(self):
        nome = self.entry_nome_tarefa.get()
        if nome:
            self.banco.adicionar_tarefa(nome)
            messagebox.showinfo("Sucesso", "Tarefa criada com sucesso.")
            self.mostrar_menu()

    def atualizar_tarefa(self):
        nome_tarefa = self.entry_nome_tarefa_atualizar.get()
        novo_nome = self.entry_novo_nome.get()
        if nome_tarefa and novo_nome:
            self.banco.atualizar_tarefa(nome_tarefa, novo_nome)
            messagebox.showinfo("Sucesso", "Tarefa atualizada com sucesso.")
            self.mostrar_menu()

    def excluir_tarefa(self):
        nome_tarefa = self.entry_nome_tarefa_excluir.get()
        if nome_tarefa:
            self.banco.excluir_tarefa(nome_tarefa)
            messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso.")
            self.mostrar_menu()

    def salvar_login(self, usuario):
        agora = datetime.datetime.now()
        with open("log.txt", "a") as arquivo:
            arquivo.write(f"Login: {usuario} - Data: {agora.strftime('%d/%m/%Y')} - Hora: {agora.strftime('%H:%M:%S')}\n")

    def carregar_login(self):
        if os.path.exists("log.txt"):
            os.remove("log.txt")  # Apaga o arquivo temporário se já existir

    def limpar_tela(self):
        for widget in self.master.winfo_children():
            widget.destroy()

root = tk.Tk()
app = InterfaceGrafica(root)
root.mainloop()


