import sqlite3

# Cria conexão com o banco de dados (se não existir, cria o arquivo)
conn = sqlite3.connect('imagens_metadata.db')
cursor = conn.cursor()

# Cria a tabela metadata_imagens
cursor.execute('''
CREATE TABLE IF NOT EXISTS metadata_imagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_imagem TEXT,
    data_captura TEXT,
    latitude REAL,
    longitude REAL,
    pasta TEXT,
    tamanho_mb REAL
);
''')

conn.commit()
conn.close()

print("Banco de dados 'imagens_metadata.db' e tabela 'metadata_imagens' criados com sucesso!")
