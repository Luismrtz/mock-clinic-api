from flask import Flask
from app.config import get_config
from app.db import db, migrate


def create_app(config_name="dev"):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.ping import ping_blueprint

    app.register_blueprint(ping_blueprint)

    return app
