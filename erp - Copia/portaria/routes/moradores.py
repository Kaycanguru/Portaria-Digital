from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, session
from .models import db, Morador, Veiculo, registrar_historico
import os, base64, json

moradores_bp = Blueprint('moradores_bp', __name__, url_prefix='/moradores')

# Listar moradores
@moradores_bp.route('/')
def listar_moradores():
    moradores_lista = Morador.query.all()
    return render_template('moradores.html', moradores=moradores_lista)

# Novo morador
@moradores_bp.route('/novo')
def novo():
    return render_template('moradores_form.html', morador=None)

# Salvar morador + veículo
@moradores_bp.route('/salvar', methods=['POST'])
def salvar():
    nome = request.form['nome_morador']
    email = request.form['email_morador']
    cpf = request.form['cpf_morador']
    telefone = request.form['telefone_morador']
    nascimento = request.form['nascimento_morador']
    apartamento = request.form['apartamento_morador']
    bloco = request.form['bloco_morador']
    moradia = request.form['moradia_morador']
    quantidade = request.form['quantidade_morador']

    # Verifica duplicados de morador
    if Morador.query.filter_by(cpf_morador=cpf).first():
        flash("Já existe morador com este CPF!", "warning")
        return redirect(url_for('moradores_bp.novo'))
    if Morador.query.filter_by(email_morador=email).first():
        flash("Já existe morador com este E-mail!", "warning")
        return redirect(url_for('moradores_bp.novo'))
    if Morador.query.filter_by(telefone_morador=telefone).first():
        flash("Já existe morador com este Telefone!", "warning")
        return redirect(url_for('moradores_bp.novo'))

    # Veículo (opcional)
    placa = request.form.get('placa')
    modelo = request.form.get('modelo')
    cor = request.form.get('cor')

    if placa and Veiculo.query.filter_by(placa=placa).first():
        flash("Já existe morador com esta Placa de veículo!", "warning")
        return redirect(url_for('moradores_bp.novo'))

    # Cria o morador
    morador = Morador(
        nome_morador=nome,
        email_morador=email,
        cpf_morador=cpf,
        telefone_morador=telefone,
        nascimento_morador=nascimento,
        apartamento_morador=apartamento,
        bloco_morador=bloco,
        moradia_morador=moradia,
        quantidade_morador=quantidade
    )

    # Foto
    foto_data = request.form.get('foto_morador_data')
    if foto_data:
        header, encoded = foto_data.split(",", 1)
        foto_bytes = base64.b64decode(encoded)
        nome_arquivo = f"{nome.replace(' ', '_')}.png"
        caminho = os.path.join(current_app.static_folder, 'uploads', nome_arquivo)
        with open(caminho, 'wb') as f:
            f.write(foto_bytes)
        morador.foto_morador = nome_arquivo

    # Face descriptor
    face_descriptor_json = request.form.get('face_descriptor')
    if face_descriptor_json:
        morador.face_descriptor = face_descriptor_json

    # Veículo (só cria se tiver placa)
    if placa:
        veiculo = Veiculo(
            placa=placa,
            modelo=modelo,
            cor=cor,
            apartamento=apartamento,
            morador=morador
        )
        db.session.add(veiculo)

    db.session.add(morador)
    db.session.commit()

    # Histórico
    nome_usuario = session.get('nome_usuario', 'Administrador')
    registrar_historico(nome_usuario, f"Cadastrou morador '{nome}'", "Moradores")

    flash("Morador cadastrado com sucesso!", "success")
    return redirect(url_for('moradores_bp.listar_moradores'))

# Editar
@moradores_bp.route('/editar/<int:id>')
def editar(id):
    morador = Morador.query.get_or_404(id)
    return render_template('moradores_form.html', morador=morador)

# Atualizar
@moradores_bp.route('/atualizar', methods=['POST'])
def atualizar():
    id = request.form['id']
    morador = Morador.query.get_or_404(id)

    morador.nome_morador = request.form['nome_morador']
    morador.email_morador = request.form['email_morador']
    morador.cpf_morador = request.form['cpf_morador']
    morador.telefone_morador = request.form['telefone_morador']
    morador.nascimento_morador = request.form['nascimento_morador']
    morador.apartamento_morador = request.form['apartamento_morador']
    morador.bloco_morador = request.form['bloco_morador']
    morador.moradia_morador = request.form['moradia_morador']
    morador.quantidade_morador = request.form['quantidade_morador']

    # Foto
    foto_data = request.form.get('foto_morador_data')
    if foto_data:
        header, encoded = foto_data.split(",", 1)
        foto_bytes = base64.b64decode(encoded)
        nome_arquivo = f"{morador.nome_morador.replace(' ', '_')}.png"
        caminho = os.path.join(current_app.static_folder, 'uploads', nome_arquivo)
        with open(caminho, 'wb') as f:
            f.write(foto_bytes)
        morador.foto_morador = nome_arquivo

    # Face descriptor
    face_descriptor_json = request.form.get('face_descriptor')
    if face_descriptor_json:
        morador.face_descriptor = face_descriptor_json

    # Veículo
    placa = request.form.get('placa')
    modelo = request.form.get('modelo')
    cor = request.form.get('cor')

    if placa:
        if morador.veiculos:
            veiculo = morador.veiculos[0]  # assume 1 veículo
            veiculo.placa = placa
            veiculo.modelo = modelo
            veiculo.cor = cor
            veiculo.apartamento = morador.apartamento_morador
        else:
            veiculo = Veiculo(
                placa=placa,
                modelo=modelo,
                cor=cor,
                apartamento=morador.apartamento_morador,
                morador=morador
            )
            db.session.add(veiculo)

    db.session.commit()

    # Histórico
    nome_usuario = session.get('nome_usuario', 'Administrador')
    registrar_historico(nome_usuario, f"Editou morador '{morador.nome_morador}'", "Moradores")

    flash("Morador atualizado com sucesso!", "success")
    return redirect(url_for('moradores_bp.listar_moradores'))

# Excluir
@moradores_bp.route('/excluir/<int:id>')
def excluir(id):
    morador = Morador.query.get_or_404(id)

    # Caminho da imagem
    if morador.foto_morador:
        caminho_foto = os.path.join(current_app.static_folder, 'uploads', morador.foto_morador)
        # Remove o arquivo se ele existir
        if os.path.exists(caminho_foto):
            os.remove(caminho_foto)

    # Exclui o morador (e automaticamente o veículo se tiver relacionamento cascade)
    # Guarda o nome antes de deletar
    nome_morador = morador.nome_morador

    db.session.delete(morador)
    db.session.commit()

    # Histórico
    nome_usuario = session.get('nome_usuario', 'Administrador')
    registrar_historico(nome_usuario, f"Excluiu morador '{nome_morador}'", "Moradores")

    flash("Morador excluído com sucesso!", "success")
    return redirect(url_for('moradores_bp.listar_moradores'))

# Rota para enviar descritores para o JS
@moradores_bp.route('/descriptors')
def get_descriptors():
    try:
        moradores = Morador.query.all()
        lista = []
        for m in moradores:
            if m.face_descriptor:  # só envia quem tem descritor
                lista.append({
                    "id": m.id,
                    "nome": m.nome_morador,
                    "descriptor": json.loads(m.face_descriptor)  # converte string JSON para array
                })
        return jsonify(lista)
    except Exception as e:
        return jsonify({"error": "Erro ao buscar descritores do banco.", "msg": str(e)}), 500
