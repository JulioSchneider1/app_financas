from app.models import db

#Se tem um comentario muito grande, o Flake8 reclama, então vou colocar o comentário aqui em cima, para não dar erro de linha muito grande AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

# Tabela de Categorias
class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200))