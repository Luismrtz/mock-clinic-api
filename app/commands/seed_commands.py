import click
from flask import current_app
from app.db import db
from app.models import Doctor


@click.command("seed-doctors")
def seed_doctors():

    with current_app.app_context():
        db.session.add_all(
            [
                Doctor(first_name="John", last_name="Wick", email="jw123@example.com"),
                Doctor(
                    first_name="Keanu", last_name="Reeves", email="kr456@example.com"
                ),
                Doctor(
                    first_name="Hayley", last_name="Williams", email="hw789@example.com"
                ),
            ]
        )
        db.session.commit()
        click.echo("Successfully seeded doctor records.")
