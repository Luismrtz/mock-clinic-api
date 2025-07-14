from flask import Flask
from app.config import get_config
from app.db import db, migrate


def create_app(config_name="dev"):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import doctor_bp

    app.register_blueprint(doctor_bp, url_prefix="/api/doctors")

    from app.commands.seed_commands import seed_doctors

    app.cli.add_command(seed_doctors)

    return app
