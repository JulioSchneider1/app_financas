import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app
from models import db, Usuario

# Configuração do banco de dados para testes
@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            user = Usuario(nome="Admin", login="admin", senha="123")
            db.session.add(user)
            db.session.commit()

        yield client

        with app.app_context():
            db.drop_all()

# Configuração do contexto do aplicativo para testes
@pytest.fixture
def app_context():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

        user = Usuario(nome="Admin", login="admin", senha="123")
        db.session.add(user)
        db.session.commit()

        yield

        db.session.remove()
        db.drop_all()