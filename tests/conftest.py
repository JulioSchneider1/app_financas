import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from models import db, Usuario


# ==============================
# FIXTURE: CLIENT (requisições HTTP)
# ==============================
@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()

        user = Usuario(nome="Admin", login="admin", senha="123")
        db.session.add(user)
        db.session.commit()

        with app.test_client() as client:
            yield client

        db.session.remove()
        db.drop_all()


# ==============================
# FIXTURE: APP CONTEXT (uso direto do banco)
# ==============================
@pytest.fixture
def app_context():
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()

        user = Usuario(nome="Admin", login="admin", senha="123")
        db.session.add(user)
        db.session.commit()

        yield app  # retorna o app caso precise

        db.session.remove()
        db.drop_all()