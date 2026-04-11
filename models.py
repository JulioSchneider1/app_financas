from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# MODELOS

# Tabela de usuários
class Usuario(db.Model):
    __tablename__ = "usuarios"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    login = db.Column(db.String(50))
    senha = db.Column(db.String(50))

# Tabela de lançamentos
class Lancamento(db.Model):
    __tablename__ = "lancamentos"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200))
    valor = db.Column(db.Float)
    tipo = db.Column(db.String(1))
    usuario_id = db.Column(db.Integer)
    data = db.Column(db.Date)
    status = db.Column(db.Boolean, default=True)