from flask import Blueprint, render_template, session, request
from .models import Veiculo, Morador  # importa também o modelo do morador

veiculos_bp = Blueprint('veiculos_bp', __name__, url_prefix='/veiculos')

@veiculos_bp.route('/', methods=['GET'])
def listar_veiculos():
    termo = request.args.get("q", "").strip()
    
    query = Veiculo.query
    if termo:
        termo_like = f"%{termo}%"
        query = query.filter(
            (Veiculo.placa.ilike(termo_like)) |
            (Veiculo.modelo.ilike(termo_like)) |
            (Veiculo.cor.ilike(termo_like)) |
            (Veiculo.morador.has(Morador.nome_morador.ilike(termo_like)))
        )

    veiculos_lista = query.all()
    total_veiculos = query.count()
    nome_usuario = session.get('nome_usuario', 'Usuário')

    return render_template(
        'veiculos.html',
        veiculos=veiculos_lista,
        total_veiculos=total_veiculos,
        nome_usuario=nome_usuario,
        termo=termo  # opcional, para reaproveitar no input
    )
