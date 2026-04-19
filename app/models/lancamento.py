from app.models import db


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
