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

# Funções do banco de dados (mantidas iguais)
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

# Funções da interface gráfica (com validação)
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
def atualizar_lista():
    for row in treeview.get_children():
        treeview.delete(row)
    for row in listar_clientes():
        treeview.insert('', tk.END, values=row)

def editar_cliente():
    selected = treeview.selection()
    if not selected:
        messagebox.showwarning("Erro", "Selecione um cliente para editar!")
        return

    id = treeview.item(selected, 'values')[0]
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    aniversario = entry_aniversario.get() or None  # Se estiver vazio, será None

    if nome and telefone:  # Agora só nome e telefone são obrigatórios
        atualizar_cliente(id, nome, telefone, aniversario)
        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        atualizar_lista()
    else:
        messagebox.showwarning("Erro", "Preencha pelo menos nome e telefone!")

def excluir_cliente_selecionado():
    selected = treeview.selection()
    if not selected:
        messagebox.showwarning("Erro", "Selecione um cliente para excluir!")
        return

    id = treeview.item(selected, 'values')[0]
    excluir_cliente(id)
    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
    atualizar_lista()

# Interface gráfica
root = tk.Tk()
root.title("Agenda de Clientes")
root.geometry("600x400")

# Campos de entrada
tk.Label(root, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Telefone:").grid(row=1, column=0, padx=10, pady=10)
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=1, column=1, padx=10, pady=10)

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