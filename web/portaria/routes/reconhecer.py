from flask import Blueprint, render_template, request, jsonify
from .models import Morador, Acesso, Codigo, AcessoVisitante, db
from datetime import datetime, timedelta

reconhecer_bp = Blueprint('reconhecer_bp', __name__, url_prefix='/reconhecer')

# Carrega a página reconhecer.html
@reconhecer_bp.route('/')
def index():
    return render_template('reconhecer.html')

# Registro do morador pelo reconhecimento facial
@reconhecer_bp.route('/registrar', methods=['POST'])
def registrar():
    # Recebe os dados enviados via JavaScript
    data = request.get_json()
    nome = data.get('nome')

    # Busca um morador com esse nome no banco
    morador = Morador.query.filter_by(nome_morador=nome).first()
    # Se não encontrou o morador, retorna erro para o front
    if not morador:
        return jsonify({'success': False, 'error': 'Morador não encontrado'}), 404
    # Cria um novo registro na tabela de Acesso
    novo_acesso = Acesso(morador_id=morador.id)
    # Salva no banco
    db.session.add(novo_acesso)
    db.session.commit()

    return jsonify({'success': True})

# Uso do código de acesso (visitante)
@reconhecer_bp.route('/codigo', methods=['POST'])
def usar_codigo():
    # Recebe dados enviados via JSON
    data = request.get_json()
    codigo_digitado = data.get("codigo")

    # Procura o código no banco, mas somente se estiver ativo
    codigo_obj = Codigo.query.filter_by(codigo=codigo_digitado, ativo=True).first()
    # Se não encontrou, o código é inválido
    if not codigo_obj:
        return jsonify({"success": False, "message": "Código inválido ou inativo"})

    # Calcula a data/hora limite de validade do código
    validade_limite = codigo_obj.data_criacao + timedelta(hours=codigo_obj.validade_horas) # Pega a data de criação do código e adiciona o tempo de validade
    # Se passou do prazo, retorna como expirado
    if datetime.now() > validade_limite: # Compara com a hora atual
        return jsonify({"success": False, "message": "Código expirado"})
    
    # Cria um registro na tabela acessos_visitantes
    registro = AcessoVisitante(
        codigo_id=codigo_obj.id,
        morador_id=codigo_obj.morador_id
    )
    db.session.add(registro)
    db.session.commit()

    # Se chegou até aqui, o código está válido e o acesso é liberado
    return jsonify({
        "success": True,
        "message": f"Acesso liberado para visitante do morador {codigo_obj.morador.nome_morador}"
    })
