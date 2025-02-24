import sqlite3

# Conecta ao banco de dados (ou cria se não existir)
conn = sqlite3.connect('clientes.db')
cursor = conn.cursor()

# Cria a tabela de clientes se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    aniversario TEXT
)
''')

conn.commit()