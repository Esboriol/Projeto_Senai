from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash, redirect, session
from database import get_db_connection

class Usuario:
    def __init__(self, usuario_id, nome, email, senha, telefone, cargo, foto):
        self.usuario_id = usuario_id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.cargo = cargo
        self.foto = foto

def register_usuarios(nome, email, telefone, cargo, foto, password):
    pw_hash = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # tentativa padrão (colunas minúsculas) — pode falhar se tabela usa "Nome" etc.
        cursor.execute(
            "INSERT INTO usuarios (nome, email, telefone, cargo, foto, senha) VALUES (%s, %s, %s, %s, %s, %s)",
            (nome, email, telefone, cargo, foto, pw_hash)
        )
        conn.commit()
    except Exception as e:
        # limpa transação abortada antes da tentativa alternativa
        try:
            conn.rollback()
        except Exception:
            pass

        try:
            # fallback PARA SUA TABELA (colunas com inicial maiúscula e entre aspas)
            cursor.execute(
                'INSERT INTO "usuarios" ("Nome", "Email", "Telefone", "Cargo", "Foto", "Senha") VALUES (%s, %s, %s, %s, %s, %s)',
                (nome, email, telefone, cargo, foto, pw_hash)
            )
            conn.commit()
        except Exception as e2:
            conn.rollback()
            print("Erro ao inserir usuário (tentativas):", e, e2)
            flash('Erro ao cadastrar usuário. Veja logs no console.', 'danger')
            cursor.close()
            conn.close()
            return redirect('/register')

    cursor.close()
    conn.close()
    flash('Cadastro realizado com sucesso! Faça login.', 'success')

def login_usuarios(usuario, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    row = None
    try:
        cursor.execute(
            "SELECT id, nome, senha FROM usuarios WHERE nome = %s OR email = %s",
            (usuario, usuario)
        )
        row = cursor.fetchone()
    except Exception as e:
        print("Erro consulta login:", e)

    cursor.close()
    conn.close()

    if row:
        # dependendo do driver, row pode ser tuple; adaptamos:
        user_id = row[0]
        nome_db = row[1]
        pw_hash = row[2]
        if check_password_hash(pw_hash, password):
            session['user_id'] = user_id
            session['username'] = nome_db
            flash('Login realizado com sucesso.', 'success')
            return redirect('/home')

    flash('Usuário ou senha inválidos.', 'danger')
    return redirect('/')