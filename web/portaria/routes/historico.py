from flask import Blueprint, render_template, request
from .models import Historico

historico_bp = Blueprint('historico_bp', __name__, url_prefix='/historico')

@historico_bp.route('/', methods=['GET'])
def listar_historico():
    # Captura o termo de busca enviado pela URL (?q=alguma coisa)
    termo = request.args.get("q", "").strip()
    query = Historico.query  # Começa uma consulta base na tabela Historico

# Se o usuário digitou algo para buscar
    if termo:
        termo_like = f"%{termo}%"
        # Filtro: busca por ação que contenham o termo
        query = query.filter(
            (Historico.usuario.ilike(termo_like)) |
            (Historico.acao.ilike(termo_like))
        )

    # Ordena os resultados por ID (do mais recente para o mais antigo)
    historico_lista = query.order_by(Historico.id.desc()).all()

    # Envia os dados para o template historico.html
    return render_template(
        'historico.html',
        historico=historico_lista,
        termo=termo
    )
    
