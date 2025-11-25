# routes/codigos.py
from flask import Blueprint, request, jsonify
from .models import Codigo, db
from datetime import datetime

codigos_bp = Blueprint('codigos_bp', __name__, url_prefix='/codigos')

@codigos_bp.route('/criar', methods=['POST'])
def criar_codigo():
    data = request.get_json() # Recebe os dados enviados pelo aplicativo via JSON
    codigo = data.get('codigo') # Extrai o código gerado no app
    morador_id = data.get('morador_id') # ID do morador logado no mobile
    validade_horas = data.get('validade_horas', 2) # Validade em horas (padrão: 2h)

    # Cria um novo registro no banco
    novo = Codigo(
        codigo=codigo,
        morador_id=morador_id,
        validade_horas=validade_horas
    )
    # Salva no banco de dados
    db.session.add(novo)
    db.session.commit()
    # Retorna resposta ao app
    return jsonify({"success": True, "codigo": codigo, "validade_horas": validade_horas})