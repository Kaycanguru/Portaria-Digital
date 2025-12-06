from flask import Flask
from routes.models import db
from flask_cors import CORS  # pip install flask-cors - # Biblioteca que permite requisições externas (ex: app mobile, Flet)
import os

# Importação dos blueprints, organiza o sistema em partes
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.moradores import moradores_bp
from routes.veiculos import veiculos_bp
from routes.reconhecer import reconhecer_bp
from routes.historico import historico_bp
from routes.codigos import codigos_bp
from routes.notificacoes import notificacoes_bp

# Inicializa o banco, conectando a aplicação Flask ao MySQL
from database.db_connection import init_db

# Aplicação Flask é criada
app = Flask(__name__)
init_db(app)
app.secret_key = "sua_chave_secreta_1234"

# Habilita CORS apenas para o Flet
CORS(app)

# Configura onde arquivos enviados (upload) serão armazenados
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuram a conexão com o banco de dados MySQL usando a biblioteca SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senai%40118@localhost/portaria'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/portaria'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy com a aplicação
db.init_app(app)

# Registros do módulo Blueprint (bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(moradores_bp)
app.register_blueprint(veiculos_bp)
app.register_blueprint(reconhecer_bp)
app.register_blueprint(historico_bp)
app.register_blueprint(codigos_bp)
app.register_blueprint(notificacoes_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# http://localhost:5000/reconhecer - para acessar o reconhecimento