from flask import Flask, render_template, redirect, request
from models.chamado import *
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os

UPLOADS_PHOTO = 'photos'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADS_PHOTO

@app.route('/photos/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOADS_PHOTO, filename)

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

@app.route('/photo/<filename>')
def get_photo(filename):
    filename = filename.replace('photos\\', '')
    return send_from_directory('photos', filename)


@app.route("/removerImagem", methods=["POST"])
def remover_imagem():
    chamado_id = request.json.get('chamado_id')

    if chamado_id is None:
        return {"success": False, "message": "Chamado ID é obrigatório"}, 400

    # Conecta ao banco de dados e remove a referência da imagem
    conn = get_db_connection()
    cursor = conn.cursor()

    # Primeiro, pega o caminho da imagem atual para deletá-la do sistema de arquivos
    cursor.execute("SELECT photo_path FROM chamados WHERE id = %s", (chamado_id,))
    photo_path = cursor.fetchone()

    if photo_path is None:
        return {"success": False, "message": "Imagem não encontrada"}, 404

    photo_path = photo_path[0]  # Caminho da imagem no banco de dados

    # Remover a imagem do banco de dados
    cursor.execute("UPDATE chamados SET photo_path = NULL WHERE id = %s", (chamado_id,))
    conn.commit()

    # Deletar a imagem do sistema de arquivos (caso necessário)
    try:
        if os.path.exists(photo_path):
            os.remove(photo_path)
        else:
            print(f"Arquivo {photo_path} não encontrado no sistema.")
    except Exception as e:
        print(f"Erro ao deletar a imagem: {e}")

    cursor.close()
    conn.close()

    return {"success": True}, 200

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
    return render_template("home.html")

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

@app.route("/salvarChamado", methods=["POST"])
def salvarChamado():
    if 'photo_post' in request.files:

        photo = request.files['photo_post']
        photo_name = secure_filename(photo.filename)
        photo_path = os.path.join(UPLOADS_PHOTO, photo_name)
        photo.save(photo_path)

        email_solicitante = request.form["email_requisitante"]
        nome_solicitante = request.form["nome_requisitante"]
        ambiente = request.form["ambiente"]
        descricao_chamado = request.form["descricao_chamado"]
        salvar(nome_solicitante, email_solicitante, ambiente, descricao_chamado, photo_path)
        return render_template("obrigado.html")

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    password = request.form["password"]

    if usuario == 'fernandocaum' and password == 'senai':
        return render_template("home.html")
    else:
        return render_template('index.html')


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
