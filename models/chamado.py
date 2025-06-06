from database import get_db_connection
from typing import List


class Chamado:
    def __init__(self, chamado_id, titulo, descricao, data, status, local, observacao, nome_solicitante, email_solicitante, Photo_path):
        self.chamado_id = chamado_id
        self.titulo = titulo
        self.descricao = descricao
        self.data = data
        self.status = status
        self.local = local
        self.observacao = observacao
        self.nome_solicitante = nome_solicitante
        self.email_solicitante = email_solicitante
        self.Photo_path = Photo_path

def get_chamados_by_status(status) -> List[Chamado]:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Alterando para incluir o campo photo_path na consulta
    if status == None:
        cursor.execute('SELECT id, titulo, descricao, data, status, local, observacao, photo_path FROM chamados;')
    elif status == 'ongoing':
        cursor.execute("SELECT id, titulo, descricao, data, status, local, observacao, photo_path FROM chamados WHERE status = 'ongoing';")
    elif status == 'finished':
        cursor.execute("SELECT id, titulo, descricao, data, status, local, observacao, photo_path FROM chamados WHERE status = 'finished';")
    elif status == 'most-urgent':
        cursor.execute("SELECT id, titulo, descricao, data, status, local, observacao, photo_path FROM chamados WHERE status = 'most-urgent';")
    elif status == 'urgent':
        cursor.execute("SELECT id, titulo, descricao, data, status, local, observacao, photo_path FROM chamados WHERE status = 'urgent';")
    elif status == 'common':
        cursor.execute("SELECT id, titulo, descricao, data, status, local, observacao, photo_path FROM chamados WHERE status = 'common';")
    elif status == 'no-status':
        cursor.execute("SELECT id, titulo, descricao, data, status, local, observacao, photo_path FROM chamados WHERE status = 'no-status';")

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    chamados = []

    for result in results:
        observacao = result[6]
        if observacao is None:
            observacao = ""

        chamado = Chamado(
            chamado_id=result[0],
            titulo=result[1],
            descricao=result[2],
            data=result[3],
            status=result[4],
            local=result[5],
            observacao=observacao,
            nome_solicitante="",
            email_solicitante="",
            Photo_path=result[7]  # Atualizando para pegar o photo_path
        )
        chamados.append(chamado)
    return chamados

def POSTChamado(chamado_id, observacao, status, photo_path=None):
    conn = get_db_connection()
    cur = conn.cursor()

    if photo_path:
        sql = """
            UPDATE chamados
            SET observacao = %s, status = %s, photo_path = %s
            WHERE id = %s
        """
        cur.execute(sql, (observacao, status, photo_path, chamado_id))
    else:
        sql = """
            UPDATE chamados
            SET observacao = %s, status = %s
            WHERE id = %s
        """
        cur.execute(sql, (observacao, status, chamado_id))

    conn.commit()
    cur.close()
    conn.close()

def salvar(nome, email, ambiente, descricao, photo_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    from datetime import datetime
    data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """
        INSERT into chamados (nome_solicitante, email_solicitante, local, descricao, titulo, data, status, photo_path) VALUES (%s, %s, %s,%s, %s, %s, %s, %s);
        """, (nome, email, ambiente, descricao, "Chamado", data_hora_atual, "no-status", photo_path)
    )
    conn.commit()
    conn.close()
