from app import create_app
from app.models import db, Usuario

app = create_app()

with app.app_context():
    user = Usuario.query.filter_by(login="admin").first()

    if not user:
        user = Usuario(
            nome="Admin",
            login="admin",
            senha="123",
            email="julio.schneider1@universo.univates.br",
        )

        db.session.add(user)
        db.session.commit()

        print("✔ Usuário admin criado")
    else:
        print("✔ Usuário admin já existe")
