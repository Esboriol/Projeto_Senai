from database import get_db_connection

conn = get_db_connection()

conn.autocommit = True  # Necessário para criar uma nova tabela
cur = conn.cursor()


create_table_query = """
CREATE TABLE chamados (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    nome_solicitante VARCHAR(255) NOT NULL,
    email_solicitante VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    local VARCHAR(55),
    status VARCHAR(50),
    observacao VARCHAR(255)

);
"""

# create_table_query = """
# DROP TABLE chamados;
# """
#
# # Execute o comando SQL
try:
    cur.execute(create_table_query)
    print("Tabela 'chamados' criada com sucesso.")
except Exception as e:
    print(f"Erro ao criar a tabela: {e}")
finally:
    pass
    # Feche a comunicação com o banco de dados
    # cur.close()
    # conn.close()



registros = [
    ("Chamado", "Fernando Vieira", "fernandofv2@gmail.com", "Fiação elétrica exposta no corredor principal. Precisa de inspeção imediata para evitar riscos de choque.", "2024-08-22 09:00:00", "most-urgent", "Corredor Principal"),
    ("Chamado", "José Fagundes", "josefagundes@hotmail.com", "Vazamento na tubulação do banheiro. Verificar e reparar a tubulação para evitar danos maiores.", "2024-08-22 10:00:00", "urgent", "Banheiro"),
    ("Chamado", "Pedro Carrilho", "c.pedro23@gmail.com", "Janela do escritório com problema de fechamento. Substituir ou ajustar o mecanismo de fechamento.", "2024-08-22 11:00:00", "common", "Escritório"),
]



# Comando SQL para inserir registros
insert_query = """
INSERT INTO chamados (titulo, nome_solicitante, email_solicitante, descricao, data, status, local)
VALUES (%s, %s, %s,%s, %s, %s, %s);
"""

try:
    cur.executemany(insert_query, registros)
    print("Registros inseridos com sucesso.")
except Exception as e:
    print(f"Erro ao inserir registros: {e}")
finally:
    # Feche a comunicação com o banco de dados
    cur.close()
    conn.close()