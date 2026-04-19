from app.models import db


# Tabela de usuários
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    login = db.Column(db.String(50))
    senha = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=True)
