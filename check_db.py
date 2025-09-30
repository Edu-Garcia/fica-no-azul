import sqlite3

DB_NAME = "dashboard.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Listar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tabelas encontradas no banco:")
for t in tables:
    print("-", t[0])

# (Opcional) Mostrar colunas de cada tabela
for t in tables:
    cursor.execute(f"PRAGMA table_info({t[0]});")
    cols = cursor.fetchall()
    print(f"\nEstrutura da tabela {t[0]}:")
    for col in cols:
        print(" ", col)

conn.close()