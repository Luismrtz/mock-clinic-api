from app.db import db
from app.models import Doctor


def seed_doctors():
    rows = [
        Doctor(first_name="John", last_name="Wick", email="jw123@example.com"),
        Doctor(first_name="Keanu", last_name="Reeves", email="kr456@example.com"),
        Doctor(first_name="Hayley", last_name="Williams", email="hw789@example.com"),
    ]
    db.session.add_all(rows)
    db.session.flush()
    return rows
