from flask import Blueprint, render_template, request, jsonify
from .models import Morador, Acesso, Codigo, AcessoVisitante, db
from datetime import datetime, timedelta

reconhecer_bp = Blueprint('reconhecer_bp', __name__, url_prefix='/reconhecer')

# Tela principal do reconhecimento
@reconhecer_bp.route('/')
def index():
    return render_template('reconhecer.html')

# Registro do morador pelo reconhecimento facial
@reconhecer_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    nome = data.get('nome')

    morador = Morador.query.filter_by(nome_morador=nome).first()
    if not morador:
        return jsonify({'success': False, 'error': 'Morador não encontrado'}), 404

    novo_acesso = Acesso(morador_id=morador.id)
    db.session.add(novo_acesso)
    db.session.commit()

    return jsonify({'success': True})

# Uso do código de acesso (visitante)
@reconhecer_bp.route('/codigo', methods=['POST'])
def usar_codigo():
    data = request.get_json()
    codigo_digitado = data.get("codigo")

    # busca código ativo
    codigo_obj = Codigo.query.filter_by(codigo=codigo_digitado, ativo=True).first()
    if not codigo_obj:
        return jsonify({"success": False, "message": "Código inválido ou inativo"})

    # verifica validade
    validade_limite = codigo_obj.data_criacao + timedelta(hours=codigo_obj.validade_horas)
    if datetime.utcnow() > validade_limite:
        return jsonify({"success": False, "message": "Código expirado"})

    # se chegou aqui, o código é válido
    return jsonify({
        "success": True,
        "message": f"Acesso liberado para visitante do morador {codigo_obj.morador.nome_morador}"
    })
