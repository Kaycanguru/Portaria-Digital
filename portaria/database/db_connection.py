# db_connection.py: Conexão com Banco de Dados
# pip install flask_mysqldb

from flask_mysqldb import MySQL
from flask import current_app

mysql = MySQL()

# Função para conexão com o banco de dados
def init_db(app):
    app.config['MYSQL_HOST'] = '127.0.0.1'       # Acesso ao servidor local
    app.config['MYSQL_USER'] = 'root'            # Usuário do banco de dados
    app.config['MYSQL_PASSWORD'] = 'Senai@118'   # Senha do Banco de Dados
    app.config['MYSQL_DB'] = 'portaria'       # Nome do Banco de Dados
    mysql.init_app(app)