import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class GerenciadorProjetos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Projetos")
        self.root.geometry("400x400")  # Ajustando o tamanho da janela

        # Conectar ao banco de dados SQLite
        self.conexao = sqlite3.connect("project_zeus.db")
        self.criar_tabela()

        # Interface gráfica
        self.iniciar_interface()

    def criar_tabela(self):
        # Criar tabela se não existir
        cursor = self.conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projetos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                status TEXT NOT NULL DEFAULT 'Iniciar',
                tarefa TEXT,
                descricao_tarefa TEXT,
                data_finalizacao TEXT
            )
        ''')
        self.conexao.commit()

    def iniciar_interface(self):
        # Componentes da interface
        self.label_nome = tk.Label(self.root, text="Nome do Projeto:")
        self.entry_nome = tk.Entry(self.root, width=30)

        self.label_descricao = tk.Label(self.root, text="Descrição:")
        self.entry_descricao = tk.Entry(self.root, width=30)

        self.label_status = tk.Label(self.root, text="Status:")
        self.status_var = tk.StringVar(self.root)
        self.status_var.set("Iniciar")  # Valor padrão
        self.entry_status = tk.OptionMenu(self.root, self.status_var, "Iniciar", "Em andamento", "Finalizado")

        self.label_tarefa = tk.Label(self.root, text="Tarefa:")
        self.entry_tarefa = tk.Entry(self.root, width=30)

        self.label_descricao_tarefa = tk.Label(self.root, text="Descrição da Tarefa:")
        self.entry_descricao_tarefa = tk.Entry(self.root, width=30)

        self.label_data_finalizacao = tk.Label(self.root, text="Data de Finalização:")
        self.entry_data_finalizacao = tk.Entry(self.root, width=15)

        self.botao_iniciar = tk.Button(self.root, text="Iniciar Projeto", command=self.iniciar_projeto)
        self.botao_consultar = tk.Button(self.root, text="Consultar Projetos", command=self.exibir_resultados)
        self.botao_deletar = tk.Button(self.root, text="Deletar Projetos", command=self.deletar_projetos)

        # Posicionamento na tela
        self.label_nome.grid(row=0, column=0, pady=5)
        self.entry_nome.grid(row=0, column=1, pady=5)

        self.label_descricao.grid(row=1, column=0, pady=5)
        self.entry_descricao.grid(row=1, column=1, pady=5)

        self.label_status.grid(row=2, column=0, pady=5)
        self.entry_status.grid(row=2, column=1, pady=5)

        self.label_tarefa.grid(row=3, column=0, pady=5)
        self.entry_tarefa.grid(row=3, column=1, pady=5)

        self.label_descricao_tarefa.grid(row=4, column=0, pady=5)
        self.entry_descricao_tarefa.grid(row=4, column=1, pady=5)

        self.label_data_finalizacao.grid(row=5, column=0, pady=5)
        self.entry_data_finalizacao.grid(row=5, column=1, pady=5)

        self.botao_iniciar.grid(row=6, column=0, columnspan=2, pady=10)
        self.botao_consultar.grid(row=7, column=0, columnspan=2, pady=10)
        self.botao_deletar.grid(row=8, column=0, columnspan=2, pady=10)

    def iniciar_projeto(self):
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        status = self.status_var.get()
        tarefa = self.entry_tarefa.get()
        descricao_tarefa = self.entry_descricao_tarefa.get()
        data_finalizacao = self.entry_data_finalizacao.get()

        if nome:
            cursor = self.conexao.cursor()
            cursor.execute("INSERT INTO projetos (nome, descricao, status, tarefa, descricao_tarefa, data_finalizacao) VALUES (?, ?, ?, ?, ?, ?)",
                           (nome, descricao, status, tarefa, descricao_tarefa, data_finalizacao))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Projeto iniciado com sucesso!")
        else:
            messagebox.showerror("Erro", "O nome do projeto não pode estar vazio.")

    def exibir_resultados(self):
        # Cria uma nova janela para exibir os resultados
        resultados_janela = tk.Toplevel(self.root)
        resultados_janela.title("Projetos")

        # Cria um Text widget para exibir os resultados
        resultado_text = tk.Text(resultados_janela, width=40, height=10)
        resultado_text.pack(padx=10, pady=10)

        # Recupera os dados do banco de dados
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM projetos")
        projetos = cursor.fetchall()

        # Adiciona os resultados ao Text widget
        for projeto in projetos:
            resultado_text.insert(tk.END, f"ID: {projeto[0]}\n")
            resultado_text.insert(tk.END, f"Nome: {projeto[1]}\n")
            resultado_text.insert(tk.END, f"Descrição: {projeto[2]}\n")
            resultado_text.insert(tk.END, f"Status: {projeto[3]}\n")
            resultado_text.insert(tk.END, f"Tarefa: {projeto[4]}\n")
            resultado_text.insert(tk.END, f"Descrição da Tarefa: {projeto[5]}\n")
            resultado_text.insert(tk.END, f"Data de Finalização: {projeto[6]}\n\n")

    def deletar_projetos(self):
        # Pede ao usuário para digitar o ID do projeto a ser excluído
        id_projeto = simpledialog.askinteger("Deletar Projeto", "Digite o ID do projeto a ser deletado:")

        if id_projeto is not None:
            # Tenta deletar o projeto com o ID fornecido
            cursor = self.conexao.cursor()
            cursor.execute("DELETE FROM projetos WHERE id=?", (id_projeto,))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", f"Projeto com ID {id_projeto} deletado com sucesso!")
        else:
            messagebox.showerror("Erro", "ID inválido.")
if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorProjetos(root)
    root.mainloop()
