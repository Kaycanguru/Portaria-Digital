from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

db = SQLAlchemy()

# relationship serve para o Python entender o relacionamento entre os objetos (classes) e facilitar o acesso entre eles

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(255), nullable=False)
    email_usuario = db.Column(db.String(255), nullable=False, unique=True)
    senha_usuario = db.Column(db.String(255), nullable=False)

class Morador(db.Model):
    __tablename__ = 'moradores'
    id = db.Column(db.Integer, primary_key=True)
    nome_morador = db.Column(db.String(255), nullable=False) 
    email_morador = db.Column(db.String(255), nullable=False, unique=True)
    cpf_morador = db.Column(db.String(255), nullable=False, unique=True)
    telefone_morador = db.Column(db.String(255), nullable=False, unique=True)
    nascimento_morador = db.Column(db.Date, nullable=False)
    apartamento_morador = db.Column(db.String(255), nullable=False)
    bloco_morador = db.Column(db.String(255), nullable=False)
    moradia_morador = db.Column(db.String(255), nullable=False)
    quantidade_morador = db.Column(db.String(255), nullable=False)
    foto_morador = db.Column(db.String(255), nullable=True)
    face_descriptor = db.Column(db.Text, nullable=True)

    # Relacionamento 1:N
    veiculos = db.relationship(
        'Veiculo', back_populates='morador', cascade="all, delete-orphan"
    )

    def get_descriptor(self):
        if not self.face_descriptor:
            return None
        return json.loads(self.face_descriptor)

class Veiculo(db.Model):
    __tablename__ = 'veiculos'
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), nullable=False, unique=True)
    modelo = db.Column(db.String(50), nullable=True)
    cor = db.Column(db.String(30), nullable=True)
    apartamento = db.Column(db.String(50), nullable=False)

    morador_id = db.Column(db.Integer, db.ForeignKey('moradores.id'))
    morador = db.relationship('Morador', back_populates='veiculos')

class Historico(db.Model):
    __tablename__ = 'historico'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(255), nullable=False)
    acao = db.Column(db.String(255), nullable=False)
    entidade = db.Column(db.String(100), nullable=False)
    data_registro = db.Column(db.Date, nullable=False)
    hora_registro = db.Column(db.Time, nullable=False)

    def __init__(self, usuario, acao, entidade):
        agora = datetime.now()
        self.usuario = usuario
        self.acao = acao
        self.entidade = entidade
        self.data_registro = agora.date()
        self.hora_registro = agora.time()

def registrar_historico(usuario, acao, entidade):
    novo = Historico(usuario=usuario, acao=acao, entidade=entidade)
    db.session.add(novo)
    db.session.commit()

class Acesso(db.Model):
    __tablename__ = 'acessos'
    id = db.Column(db.Integer, primary_key=True)
    morador_id = db.Column(db.Integer, db.ForeignKey('moradores.id'), nullable=False)
    data_registro = db.Column(db.Date, nullable=False)
    hora_registro = db.Column(db.Time, nullable=False)

    morador = db.relationship('Morador', backref='acessos')

    def __init__(self, morador_id):
        agora = datetime.now()
        self.morador_id = morador_id
        self.data_registro = agora.date()
        self.hora_registro = agora.time()

def registrar_acesso(morador):
    novo_acesso = Acesso(morador_id=morador.id)
    db.session.add(novo_acesso)
    db.session.commit()

class Codigo(db.Model):
    __tablename__ = 'codigos'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), nullable=False)
    morador_id = db.Column(db.Integer, db.ForeignKey('moradores.id'), nullable=False)
    validade_horas = db.Column(db.Integer, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)

    morador = db.relationship('Morador', backref='codigos')

class AcessoVisitante(db.Model):
    __tablename__ = 'acessos_visitantes'
    id = db.Column(db.Integer, primary_key=True)
    codigo_id = db.Column(db.Integer, db.ForeignKey('codigos.id'), nullable=False)
    morador_id = db.Column(db.Integer, db.ForeignKey('moradores.id'), nullable=False)
    nome_visitante = db.Column(db.String(120))
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)

    codigo = db.relationship('Codigo', backref='usos')
    morador = db.relationship('Morador')
