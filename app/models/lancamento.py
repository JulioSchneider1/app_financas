from app.models import db

#Se tem um comentario muito grande, o Flake8 reclama, 
# então vou colocar o comentário aqui em cima, 
# para não dar erro de linha muito grande AAAAAAAAAAAAAAAAAAAAAAAA
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

# Tabela de lançamentos
class Lancamento(db.Model):
    __tablename__ = "lancamentos"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200))
    valor = db.Column(db.Float)
    tipo = db.Column(db.String(1))
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    data = db.Column(db.Date)
    status = db.Column(db.Boolean, default=True)
