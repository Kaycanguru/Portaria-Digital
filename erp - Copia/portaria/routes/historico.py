from flask import Blueprint, render_template, request
from .models import Historico

historico_bp = Blueprint('historico_bp', __name__, url_prefix='/historico')

@historico_bp.route('/', methods=['GET'])
def listar_historico():
    termo = request.args.get("q", "").strip()
    query = Historico.query

    if termo:
        termo_like = f"%{termo}%"
        query = query.filter(
            (Historico.usuario.ilike(termo_like)) |
            (Historico.acao.ilike(termo_like))
        )

    historico_lista = query.order_by(Historico.id.desc()).all()

    return render_template(
        'historico.html',
        historico=historico_lista,
        termo=termo
    )
    
