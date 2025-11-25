from flask import Flask, render_template, request, send_from_directory
from models.chamado import *   # assume get_db_connection(), get_chamados_by_status(), salvar(), POSTChamado(), ...
from werkzeug.utils import secure_filename
from models.usuario import *
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
    if 'username' not in session:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Pega a foto do usuário logado
    cursor.execute("SELECT foto FROM usuarios WHERE nome = %s", (session['username'],))
    row = cursor.fetchone()

    foto = row[0] if row and row[0] else None

    cursor.close()
    conn.close()

    return render_template("home.html", username=session.get('username'), foto=foto)


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
        salvar_chamado(nome_solicitante, email_solicitante, ambiente, descricao_chamado, photo_path)
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
    telefone = request.form.get('telefone', '').strip() or ''
    cargo = request.form.get('cargo', '').strip() or ''
    password = request.form.get('password', '')
    password2 = request.form.get('password2', '')

    if not nome or not password:
        flash('Preencha usuário e senha.', 'danger')
        return redirect('/register')
    if password != password2:
        flash('As senhas não coincidem.', 'danger')
        return redirect('/register')

    # Lida com o upload da foto
    foto_file = request.files.get('foto')
    foto_filename = ''
    if foto_file and foto_file.filename != '':
        filename = secure_filename(foto_file.filename)
        foto_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto_file.save(foto_filename)

    register_usuarios(nome, email, telefone, cargo, foto_filename, password)
    return redirect('/')


# ---- login (substitui comparação hardcoded) ----
@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario", "").strip()
    password = request.form.get("password", "")

    return login_usuarios(usuario, password)

@app.route("/editar", methods=["GET", "POST"])
def edits():
    if 'username' not in session:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()  # cursor normal, sem argumentos

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        cargo = request.form.get('cargo', '').strip()
        nova_senha = request.form.get('senha', '')
        foto_file = request.files.get('foto')

        foto_filename = None
        if foto_file and foto_file.filename != '':
            filename = secure_filename(foto_file.filename)
            foto_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto_file.save(foto_filename)

        try:
            update_fields = []
            params = []

            if nome:
                update_fields.append("nome = %s")
                params.append(nome)
            if email:
                update_fields.append("email = %s")
                params.append(email)
            if telefone:
                update_fields.append("telefone = %s")
                params.append(telefone)
            if cargo:
                update_fields.append("cargo = %s")
                params.append(cargo)
            if foto_filename:
                update_fields.append("foto = %s")
                params.append(foto_filename)
            if nova_senha:
                update_fields.append("senha = %s")
                params.append(generate_password_hash(nova_senha))

            if update_fields:
                sql = f"UPDATE usuarios SET {', '.join(update_fields)} WHERE nome = %s"
                params.append(session['username'])
                cursor.execute(sql, tuple(params))
                conn.commit()

                if nome:
                    session['username'] = nome  # atualiza sessão

                flash("Perfil atualizado com sucesso.", "success")
            else:
                flash("Nenhuma alteração feita.", "info")

        except Exception as e:
            print("Erro ao atualizar perfil:", e)
            conn.rollback()
            flash("Erro ao atualizar perfil.", "danger")

        cursor.close()
        conn.close()
        return redirect('/home')

    # GET: pegar dados do usuário logado
    cursor.execute("SELECT nome, email, telefone, cargo, foto FROM usuarios WHERE nome = %s", (session['username'],))
    row = cursor.fetchone()
    usuario = None

    if row:
        # converte a tupla row em dict usando os nomes das colunas
        cols = [desc[0] for desc in cursor.description]
        usuario = dict(zip(cols, row))

    cursor.close()
    conn.close()

    return render_template("editar.html", usuario=usuario)

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
