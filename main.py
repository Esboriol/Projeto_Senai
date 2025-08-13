from flask import Flask, render_template, redirect, request, session, flash, send_from_directory
from models.chamado import *   # assume get_db_connection(), get_chamados_by_status(), salvar(), POSTChamado(), ...
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

UPLOADS_PHOTO = 'photos'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADS_PHOTO

# SECRET_KEY para session/flash (troque para algo seguro em produção / variáveis de ambiente)
app.secret_key = os.environ.get('SECRET_KEY', 'troque_esse_valor_em_producao')

# ---- arquivos estáticos / fotos ----
@app.route('/photos/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOADS_PHOTO, filename)

@app.route('/photo/<filename>')
def get_photo(filename):
    filename = filename.replace('photos\\', '')
    return send_from_directory('photos', filename)

# ---- criação da tabela de usuários (tenta compatibilizar com PostgreSQL/MySQL/SQLite) ----
def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    created = False
    # Tenta SQL estilo PostgreSQL / MySQL
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(150) UNIQUE NOT NULL,
                email VARCHAR(200) UNIQUE,
                password_hash VARCHAR(256) NOT NULL
            )
        """)
        created = True
    except Exception:
        # tenta MySQL style
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(150) UNIQUE NOT NULL,
                    email VARCHAR(200) UNIQUE,
                    password_hash VARCHAR(256) NOT NULL
                )
            """)
            created = True
        except Exception:
            # fallback para SQLite
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE,
                        password_hash TEXT NOT NULL
                    )
                """)
                created = True
            except Exception as e:
                print("Erro ao tentar criar tabela users:", e)

    conn.commit()
    cursor.close()
    conn.close()
    return created

# ---- rotas de páginas existentes ----
@app.route("/")
def inicial():
    return render_template("index.html")

@app.route("/ts")
def testes():
    return render_template("/testes/teste.html")

@app.route("/chs")
def chamados():
    return render_template("/testes/chamados.html")

@app.route("/tbs")
def tabelas():
    return render_template("/testes/tabela.html")

@app.route("/pedidos")
def pedidos():
    chamados = get_chamados_by_status(None)
    for c in chamados:
        print(type(c.Photo_path))
    return render_template("pedidos.html", chamados=chamados)

@app.route("/chamados")
def chamado():
    return render_template("chamados.html")

@app.route("/home")
def home():
    # Se quiser restringir: redirecionar ao login se não tiver session
    if 'username' not in session:
        return redirect('/')
    return render_template("home.html", username=session.get('username'))

@app.route("/todos")
def todes():
    return render_template("/test/todos.html")

@app.route("/tabela")
def tabela():
    return render_template("tabela.html", chamados=get_chamados_by_status(None))

@app.route('/pedidosO')
def pedidosO():
    return render_template('emAndamento.html', chamados=get_chamados_by_status('ongoing'))

@app.route('/pedidosMU')
def pedidosMU():
    return render_template('muitoUrgente.html', chamados=get_chamados_by_status('most-urgent'))

@app.route('/pedidosF')
def pedidosF():
    return render_template('finalizado.html', chamados=get_chamados_by_status('finished'))

@app.route('/pedidosU')
def pedidosU():
    return render_template('urgente.html', chamados=get_chamados_by_status('urgent'))

@app.route('/pedidosC')
def pedidosC():
    return render_template('comum.html', chamados=get_chamados_by_status('common'))

@app.route('/pedidosNS')
def pedidosNS():
    return render_template('semstatus.html', chamados=get_chamados_by_status('no-status'))

@app.route("/grafico")
def grafico():
    return render_template("grafico.html", chamados=get_chamados_by_status(None))

@app.route("/form")
def form():
    return render_template("form.html")

# ---- salvar chamado: integra nome do solicitante com session (se houver) ----
@app.route("/salvarChamado", methods=["POST"])
def salvarChamado():
    # guarda foto (se houver)
    if 'photo_post' in request.files:
        photo = request.files['photo_post']
        photo_name = secure_filename(photo.filename)
        photo_path = os.path.join(UPLOADS_PHOTO, photo_name)
        photo.save(photo_path)

        # se usuário logado, usa o username como solicitante
        if 'username' in session:
            nome_solicitante = session.get('username')
            email_solicitante = request.form.get("email_requisitante", "")
        else:
            email_solicitante = request.form.get("email_requisitante", "")
            nome_solicitante = request.form.get("nome_requisitante", "")

        ambiente = request.form.get("ambiente", "")
        descricao_chamado = request.form.get("descricao_chamado", "")
        # A função salvar(nome, email, ambiente, descricao, photo_path) deve existir em models.chamado
        salvar(nome_solicitante, email_solicitante, ambiente, descricao_chamado, photo_path)
        return render_template("obrigado.html")
    # se não houver arquivo (opcional)
    flash("Nenhuma foto enviada.", "warning")
    return redirect("/form")

# ---- registrar usuário ----
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    nome = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip() or None
    telefone = request.form.get('telefone', '').strip() or ''   # se não enviar, salva string vazia
    cargo = request.form.get('cargo', '').strip() or ''         # se não enviar, salva string vazia
    foto = request.form.get('foto', '').strip() or ''           # campo opcional (path ou url)
    password = request.form.get('password', '')
    password2 = request.form.get('password2', '')

    if not nome or not password:
        flash('Preencha usuário e senha.', 'danger')
        return redirect('/register')
    if password != password2:
        flash('As senhas não coincidem.', 'danger')
        return redirect('/register')

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
    return redirect('/')

# ---- login (substitui comparação hardcoded) ----
@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario", "").strip()  # pode ser nome ou e-mail
    password = request.form.get("password", "")

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
        # fallback para colunas que foram criadas com nomes entre aspas (ex.: "Nome")
        try:
            cursor.execute(
                'SELECT "Id", "Nome", "Senha" FROM "usuarios" WHERE "Nome" = %s OR "Email" = %s',
                (usuario, usuario)
            )
            row = cursor.fetchone()
        except Exception as e2:
            print("Erro consulta login:", e, e2)

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
    return render_template('index.html')

# ---- logout ----
@app.route('/logout')
def logout():
    session.clear()
    flash('Desconectado.', 'info')
    return redirect('/')

# ---- atualizar chamado (mantive sua lógica) ----
@app.route("/atualizarChamado/<pagina>", methods=["POST"])
def atualizarChamado(pagina):
    chamadoId = request.form['chamado_id']
    observacao = request.form['observacao']
    status = request.form['status']
    imagem = request.files.get('imagem')
    image_path = None
    if imagem and imagem.filename != '':
        filename = secure_filename(imagem.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imagem.save(image_path)
    POSTChamado(chamadoId, observacao, status, image_path)
    if pagina == 'todos':
        return redirect("/pedidos")
    elif pagina == 'andamento':
        return redirect("/pedidosO")
    elif pagina == 'comum':
        return redirect("/pedidosC")
    elif pagina == 'finalizado':
        return redirect("/pedidosF")
    elif pagina == "muitoUrgente":
        return redirect("/pedidosMU")
    elif pagina == "semStatus":
        return redirect("/pedidosNS")
    elif pagina == "urgente":
        return redirect("/pedidosU")

if __name__ == '__main__':
    app.run(debug=True)
