from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Aluno(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    turma = db.Column(db.String(20), nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)

class Progresso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    desafio_id = db.Column(db.String(50), nullable=False)
    tentativas = db.Column(db.Integer, default=0)
    nota = db.Column(db.Integer, default=0)
    last_code = db.Column(db.Text)