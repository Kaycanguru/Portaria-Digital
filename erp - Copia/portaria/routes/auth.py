from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db_connection import mysql
import MySQLdb.cursors

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha_usuario = request.form['senha_usuario']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE nome_usuario = %s AND senha_usuario = %s', (nome_usuario, senha_usuario))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['nome_usuario'] = account['nome_usuario']
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Usuário ou senha inválidos!', 'danger')

    # Este return é obrigatório para GET ou falha no login
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))  # Redireciona para a tela de login
