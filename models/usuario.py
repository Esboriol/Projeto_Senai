from database import get_db_connection
from typing import List

class Usuario:
    def __init__(self, usuario_id, nome, email, senha, telefone, cargo, foto):
        self.usuario_id = usuario_id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.cargo = cargo
        self.foto = foto
