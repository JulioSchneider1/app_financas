from app.models import db


# Tabela de Tipos
class Tipo(db.Model):
    __tablename__ = "Tipo"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200))
