from flask import Flask
from routes.models import db
from flask_cors import CORS  # <--- importar CORS (pip install flask-cors) para o sistema reconhecer o código
import os

# Importação dos blueprints, organiza o sistema em partes
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.moradores import moradores_bp
from routes.veiculos import veiculos_bp
from routes.reconhecer import reconhecer_bp
from routes.historico import historico_bp
from routes.codigos import codigos_bp

# Inicializa o banco, conectando a aplicação Flask ao MySQL
from database.db_connection import init_db

# Aplicação Flask é criada
app = Flask(__name__)
init_db(app)
app.secret_key = "sua_chave_secreta_1234"

# Habilita CORS apenas para o Flet
CORS(app)  # libera todas as origens

# Configuração de upload
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuram a conexão com o banco de dados MySQL usando a biblioteca SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senai%40118@localhost/portaria'
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# http://localhost:5000/reconhecer - para acessar o reconhecimento

# debug=True permite ver mensagens de erro e atualizações automáticas.

# Para o face recognition funcionar, nao foi instalado nada extra

# FOI FEITO:

# INSTALEI pip install Flask-Mail

# A captura + cálculo do descritor é feito no JS (face-api.js).
# O backend só recebe a string JSON com o descritor e salva no banco.

# GitHub - foi pego os arquivos de pesos (models).
# unpkg (npm) - foi pego o arquivo da biblioteca face-api.js pronta para navegador.
        # <script defer src="https://unpkg.com/face-api.js@0.22.2/dist/face-api.min.js"></script>

# 1 - O arquivo face-api.min.js que foi usado no HTML veio do npm, carregado via CDN unpkg.
# 2 - Os arquivos de pesos (.json e .bin) foram pegos do GitHub do autor e colocados na pasta do projeto.
# 3 - O cálculo do descritor facial acontece no navegador, feito pelo face-api.js usando esses pesos.
# 4 - O backend Flask não faz reconhecimento, ele só recebe o descritor em formato JSON e salva no banco.

# CDN - O unpkg é uma CDN (Content Delivery Network) gratuita que serve arquivos públicos do npm (Node Package Manager).
# npm é o Node Package Manage - LOJA DE CODIGOS PRONTOS