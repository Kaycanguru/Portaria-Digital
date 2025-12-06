from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from .models import Morador, Veiculo, Acesso, db, AcessoVisitante
from datetime import datetime, timedelta, date

dashboard_bp = Blueprint('dashboard', __name__)

# Primeiro verifica se o usuário está logado via session. Se não, redireciona para a tela de login.
@dashboard_bp.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('auth.login'))
    # Cards
    total_moradores = Morador.query.count()
    total_veiculos = Veiculo.query.count()
    nome_usuario = session['nome_usuario']

    # Últimos 10 acessos de moradores e visitantes
    acessos_moradores = Acesso.query.order_by(Acesso.id.desc()).limit(10).all()
    acessos_visitantes = AcessoVisitante.query.order_by(AcessoVisitante.id.desc()).limit(10).all()
    # Criar lista unificada normalizada
    acessos_recentes = []

    # Acessos recentes por reconhecimento facial - Lista de Moradores
    for a in acessos_moradores:
        acessos_recentes.append({
            "tipo": "morador",
            "nome": a.morador.nome_morador,
            "apto": a.morador.apartamento_morador,
            "data": a.data_registro.strftime('%d/%m'),
            "hora": a.hora_registro.strftime('%H:%M'),
            "codigo": None
        })

    # Acessos recentes por código - Lista de Visitantes
    for v in acessos_visitantes:
        acessos_recentes.append({
            "tipo": "visitante",
            "nome": None,
            "apto": None,
            "data": v.data_hora.strftime('%d/%m'),
            "hora": v.data_hora.strftime('%H:%M'),
            "codigo": v.codigo_id
        })

    # Ordenar por data e hora (mais recente primeiro)
    acessos_recentes = sorted(
        acessos_recentes,
        key=lambda x: (x["data"], x["hora"]),
        reverse=True
    )[:10]

    # Visitantes do dia
    hoje = date.today()
    visitantes_hoje = AcessoVisitante.query.filter(
        db.func.date(AcessoVisitante.data_hora) == hoje
    ).count()

    # No final da função, esses valores são enviados ao template
    return render_template(
        'dashboard.html',
        nome_usuario=nome_usuario,
        total_moradores=total_moradores,
        total_veiculos=total_veiculos,
        acessos_recentes=acessos_recentes,
        visitantes_hoje=visitantes_hoje
    )

# Rota que retorna dados do gráfico em JSON
@dashboard_bp.route('/dashboard/dados_grafico')
def dados_grafico():
    dias = 7 # define que serão 7 dias
    hoje = datetime.now().date() # calcula a data de hoje
    inicio = hoje - timedelta(days=dias - 1) # Calcula a data inicial (hoje - 6 dias)

    # Busca acessos de moradores
    resultados_moradores = (
        db.session.query(Acesso.data_registro, db.func.count(Acesso.id))
        .filter(Acesso.data_registro.between(inicio, hoje))
        .group_by(Acesso.data_registro)
        .order_by(Acesso.data_registro)
        .all()
    )

    acessos_moradores = {r[0]: r[1] for r in resultados_moradores}

    # Busca acessos de visitantes (código)
    resultados_visitantes = (
        db.session.query(db.func.date(AcessoVisitante.data_hora), db.func.count(AcessoVisitante.id)) # seleciona data e quantidade de acessos
        .filter(db.func.date(AcessoVisitante.data_hora).between(inicio, hoje)) # pega somente os acessos dentro dos últimos 7 dias
        .group_by(db.func.date(AcessoVisitante.data_hora)) # agrupa por data
        .order_by(db.func.date(AcessoVisitante.data_hora)) # conta quantos acessos teve por dia
        .all()
    )

    acessos_visitantes = {r[0]: r[1] for r in resultados_visitantes}

    # UNIFICA MORADORES + VISITANTES - Monta lista de todas as datas
    todas_as_datas = [inicio + timedelta(days=i) for i in range(dias)]

    labels = [data.strftime('%d/%m') for data in todas_as_datas] # Constrói os labels (datas no gráfico)
    valores = [ # Soma morador + visitante
        acessos_moradores.get(data, 0) + acessos_visitantes.get(data, 0)
        for data in todas_as_datas
    ]

    return jsonify({'labels': labels, 'valores': valores})