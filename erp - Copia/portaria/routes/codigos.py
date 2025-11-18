# routes/codigos.py
from flask import Blueprint, request, jsonify
from .models import Codigo, db
from datetime import datetime

codigos_bp = Blueprint('codigos_bp', __name__, url_prefix='/codigos')

@codigos_bp.route('/criar', methods=['POST'])
def criar_codigo():
    data = request.get_json()
    codigo = data.get('codigo')
    morador_id = data.get('morador_id')
    validade_horas = data.get('validade_horas', 2)

    novo = Codigo(
        codigo=codigo,
        morador_id=morador_id,
        validade_horas=validade_horas
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({"success": True, "codigo": codigo, "validade_horas": validade_horas})
