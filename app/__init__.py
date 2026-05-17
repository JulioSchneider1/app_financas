from flask import Flask
from app.models import db
from flask_migrate import Migrate
import config

migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(config)

    db.init_app(app)

    migrate.init_app(app, db)

    from app.routes import init_routes

    init_routes(app)

    return app
