import uuid
from app.db import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Uuid, primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


def __repr__(self):
    return f"<Doctor {self.first_name} {self.last_name}>"
