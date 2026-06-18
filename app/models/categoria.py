from app.models import db


# Tabela de Categorias
class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200))
