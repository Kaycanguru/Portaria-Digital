from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from .models import Morador, Veiculo, Acesso, db
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))

    total_moradores = Morador.query.count()
    total_veiculos = Veiculo.query.count()
    nome_usuario = session['nome_usuario']

    acessos_recentes = Acesso.query.order_by(Acesso.id.desc()).limit(10).all()

    return render_template(
        'dashboard.html',
        nome_usuario=nome_usuario,
        total_moradores=total_moradores,
        total_veiculos=total_veiculos,
        acessos_recentes=acessos_recentes
    )

# 🔹 Nova rota que retorna dados do gráfico em JSON
@dashboard_bp.route('/dashboard/dados_grafico')
def dados_grafico():
    dias = 7
    hoje = datetime.now().date()
    inicio = hoje - timedelta(days=dias - 1)

    # Consulta do MySQL: conta acessos por data nos últimos 7 dias
    resultados = (
        db.session.query(Acesso.data_registro, db.func.count(Acesso.id))
        .filter(Acesso.data_registro.between(inicio, hoje))
        .group_by(Acesso.data_registro)
        .order_by(Acesso.data_registro)
        .all()
    )

    # Transforma resultados em dicionário {data: total}
    acessos_por_dia = {r[0]: r[1] for r in resultados}

    # Gera todas as 7 datas (mesmo se não tiver registro no banco)
    todas_as_datas = [inicio + timedelta(days=i) for i in range(dias)]
    labels = [data.strftime('%d/%m') for data in todas_as_datas]
    valores = [acessos_por_dia.get(data, 0) for data in todas_as_datas]

    return jsonify({'labels': labels, 'valores': valores})
