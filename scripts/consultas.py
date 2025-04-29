import sqlite3
import matplotlib.pyplot as plt

def connect_db(db_path):
    return sqlite3.connect(db_path)

def imagens_por_mes(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m', data_captura) AS mes, COUNT(*) 
        FROM metadata_imagens 
        WHERE data_captura IS NOT NULL
        GROUP BY mes
        ORDER BY mes
    """)
    resultados = cursor.fetchall()
    for mes, quantidade in resultados:
        print(f"{mes}: {quantidade} imagens")
    # Gráfico
    meses = [r[0] for r in resultados]
    quantidades = [r[1] for r in resultados]
    plt.bar(meses, quantidades)
    plt.xlabel('Mês')
    plt.ylabel('Quantidade de Imagens')
    plt.title('Imagens Capturadas por Mês')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('imagens_por_mes.png')
    plt.show()

def imagens_maiores_que_3mb(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome_imagem, tamanho_mb 
        FROM metadata_imagens 
        WHERE tamanho_mb > 3
    """)
    resultados = cursor.fetchall()
    for nome, tamanho in resultados:
        print(f"{nome}: {tamanho} MB")
    # Gráfico
    tamanhos = [r[1] for r in resultados]
    plt.hist(tamanhos, bins=10, edgecolor='black')
    plt.xlabel('Tamanho (MB)')
    plt.ylabel('Quantidade de Imagens')
    plt.title('Distribuição de Tamanhos de Imagens (>3MB)')
    plt.tight_layout()
    plt.savefig('distribuicao_tamanhos.png')
    plt.show()

def quantidade_por_pasta(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pasta, COUNT(*) 
        FROM metadata_imagens 
        GROUP BY pasta
    """)
    resultados = cursor.fetchall()
    for pasta, quantidade in resultados:
        print(f"{pasta}: {quantidade} imagens")
    # Gráfico
    pastas = [r[0] for r in resultados]
    quantidades = [r[1] for r in resultados]
    plt.bar(pastas, quantidades)
    plt.xlabel('Pasta')
    plt.ylabel('Quantidade de Imagens')
    plt.title('Quantidade de Imagens por Pasta')
    plt.tight_layout()
    plt.savefig('quantidade_por_pasta.png')
    plt.show()

if __name__ == "__main__":
    db_path = "../imagens_metadata.db"
    conn = connect_db(db_path)
    print("=== Imagens por Mês ===")
    imagens_por_mes(conn)
    print("\n=== Imagens Maiores que 3MB ===")
    imagens_maiores_que_3mb(conn)
    print("\n=== Quantidade por Pasta ===")
    quantidade_por_pasta(conn)
    conn.close()
