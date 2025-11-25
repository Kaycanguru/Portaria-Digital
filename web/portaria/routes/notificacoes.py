from flask import Blueprint, render_template

notificacoes_bp = Blueprint(
    'notificacoes_bp',
    __name__,
    url_prefix='/notificacoes'
)

# Página principal de notificações
@notificacoes_bp.route('/')
def notificacoes():
    return render_template('notificacoes.html')
