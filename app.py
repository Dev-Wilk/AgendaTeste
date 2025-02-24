import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import re

# Função para validar o telefone
def validar_telefone(telefone):
    padrao = r"^\((\d{2})\)\s*(9?\d{4})-(\d{4})$"
    match = re.match(padrao, telefone)
    if not match:
        return None
    ddd, parte1, parte2 = match.groups()
    if not 11 <= int(ddd) <= 99:
        return None
    return f"{ddd}{parte1}{parte2}"

# Função para formatar o telefone
def formatar_telefone(event=None):
    texto = entry_telefone.get().replace("(", "").replace(")", "").replace(" ", "").replace("-", "")  # Remove formatação existente
    texto_formatado = ""

    # Aplica a máscara (XX) XXXXX-XXXX
    if len(texto) > 0:
        texto_formatado += f"({texto[:2]}"
    if len(texto) > 2:
        texto_formatado += f") {texto[2:7]}"
    if len(texto) > 7:
        texto_formatado += f"-{texto[7:11]}"

    # Atualiza o campo de telefone
    entry_telefone.delete(0, tk.END)
    entry_telefone.insert(0, texto_formatado)

# Função para formatar o telefone na janela de edição
def formatar_telefone_edicao(event=None):
    texto = entry_telefone_edicao.get().replace("(", "").replace(")", "").replace(" ", "").replace("-", "")  # Remove formatação existente
    texto_formatado = ""

    # Aplica a máscara (XX) XXXXX-XXXX
    if len(texto) > 0:
        texto_formatado += f"({texto[:2]}"
    if len(texto) > 2:
        texto_formatado += f") {texto[2:7]}"
    if len(texto) > 7:
        texto_formatado += f"-{texto[7:11]}"

    # Atualiza o campo de telefone na janela de edição
    entry_telefone_edicao.delete(0, tk.END)
    entry_telefone_edicao.insert(0, texto_formatado)

# Funções do banco de dados
def adicionar_cliente(nome, telefone, aniversario=None):
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (nome, telefone, aniversario) VALUES (?, ?, ?)', (nome, telefone, aniversario))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    rows = cursor.fetchall()
    conn.close()
    return rows

def atualizar_cliente(id, nome, telefone, aniversario=None):
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE clientes SET nome=?, telefone=?, aniversario=? WHERE id=?', (nome, telefone, aniversario, id))
    conn.commit()
    conn.close()

def excluir_cliente(id):
    conn = sqlite3.connect('clientes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id=?', (id,))
    conn.commit()
    conn.close()

# Funções da interface gráfica
def adicionar():
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    aniversario = entry_aniversario.get() or None

    telefone_validado = validar_telefone(telefone)
    if not telefone_validado:
        messagebox.showwarning("Erro", "Número de telefone inválido! Use o formato (DDD) 9XXXX-XXXX ou (DDD) XXXX-XXXX.")
        return

    if nome and telefone_validado:
        adicionar_cliente(nome, telefone_validado, aniversario)
        messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_aniversario.delete(0, tk.END)
        atualizar_lista()
    else:
        messagebox.showwarning("Erro", "Preencha pelo menos nome e telefone!")

def editar_cliente():
    selected = treeview.selection()
    if not selected:
        messagebox.showwarning("Erro", "Selecione um cliente para editar!")
        return

    global cliente_id
    cliente_id = treeview.item(selected, 'values')[0]
    nome = treeview.item(selected, 'values')[1]
    telefone = treeview.item(selected, 'values')[2]
    aniversario = treeview.item(selected, 'values')[3]

    def salvar_edicao():
        novo_nome = entry_nome_edicao.get()
        novo_telefone = entry_telefone_edicao.get()
        novo_aniversario = entry_aniversario_edicao.get() or None

        # Remover formatação antes da validação
        novo_telefone = novo_telefone.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")

        print(f"Telefone digitado antes da validação: {novo_telefone}")  # Depuração

        # Formatar o telefone para validação
        telefone_formatado = f"({novo_telefone[:2]}) {novo_telefone[2:7]}-{novo_telefone[7:]}"
        telefone_validado = validar_telefone(telefone_formatado)

        if not telefone_validado:
            messagebox.showwarning("Erro", "Número de telefone inválido! Use o formato (DDD) 9XXXX-XXXX ou (DDD) XXXX-XXXX.")
            return

        if novo_nome and telefone_validado:
            atualizar_cliente(int(cliente_id), novo_nome, telefone_validado, novo_aniversario)
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            atualizar_lista()
            janela_edicao.destroy()
        else:
            messagebox.showwarning("Erro", "Preencha pelo menos nome e telefone!")

    # Cria uma nova janela para edição
    janela_edicao = tk.Toplevel(root)
    janela_edicao.title("Editar Cliente")

    # Campos de entrada na janela de edição
    tk.Label(janela_edicao, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
    entry_nome_edicao = tk.Entry(janela_edicao)
    entry_nome_edicao.grid(row=0, column=1, padx=10, pady=10)
    entry_nome_edicao.insert(0, nome)

    tk.Label(janela_edicao, text="Telefone:").grid(row=1, column=0, padx=10, pady=10)
    entry_telefone_edicao = tk.Entry(janela_edicao)
    entry_telefone_edicao.grid(row=1, column=1, padx=10, pady=10)
    entry_telefone_edicao.insert(0, telefone)
    entry_telefone_edicao.bind("<KeyRelease>", formatar_telefone_edicao)

    tk.Label(janela_edicao, text="Aniversário:").grid(row=2, column=0, padx=10, pady=10)
    entry_aniversario_edicao = tk.Entry(janela_edicao)
    entry_aniversario_edicao.grid(row=2, column=1, padx=10, pady=10)
    entry_aniversario_edicao.insert(0, aniversario)

    # Botão para salvar as alterações
    tk.Button(janela_edicao, text="Salvar", command=salvar_edicao).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

def excluir_cliente_selecionado():
    # Verifica se um cliente foi selecionado
    selected = treeview.selection()
    if not selected:
        messagebox.showwarning("Erro", "Selecione um cliente para excluir!")
        return

    # Obtém o ID do cliente selecionado
    cliente_id = treeview.item(selected, 'values')[0]

    # Confirma a exclusão com o usuário
    confirmacao = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este cliente?")
    if not confirmacao:
        return  # O usuário cancelou a exclusão

    # Exclui o cliente do banco de dados
    excluir_cliente(cliente_id)
    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")

    # Atualiza a lista de clientes na interface
    atualizar_lista()

def atualizar_lista():
    for row in treeview.get_children():
        treeview.delete(row)
    for row in listar_clientes():
        treeview.insert('', tk.END, values=row)

# Interface gráfica
root = tk.Tk()
root.title("Agenda de Clientes")
root.geometry("800x500")

# Campos de entrada
tk.Label(root, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Telefone:").grid(row=1, column=0, padx=10, pady=10)
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=1, column=1, padx=10, pady=10)
entry_telefone.bind("<KeyRelease>", formatar_telefone)

tk.Label(root, text="Aniversário:").grid(row=2, column=0, padx=10, pady=10)
entry_aniversario = tk.Entry(root)
entry_aniversario.grid(row=2, column=1, padx=10, pady=10)

# Botões
tk.Button(root, text="Adicionar", command=adicionar).grid(row=3, column=0, padx=10, pady=10)
tk.Button(root, text="Editar", command=editar_cliente).grid(row=3, column=1, padx=10, pady=10)
tk.Button(root, text="Excluir", command=excluir_cliente_selecionado).grid(row=3, column=2, padx=10, pady=10)

# Lista de clientes
columns = ('id', 'nome', 'telefone', 'aniversario')
treeview = ttk.Treeview(root, columns=columns, show='headings')
treeview.heading('id', text='ID')
treeview.heading('nome', text='Nome')
treeview.heading('telefone', text='Telefone')
treeview.heading('aniversario', text='Aniversário')
treeview.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Atualiza a lista ao iniciar
atualizar_lista()

# Inicia o app
root.mainloop()