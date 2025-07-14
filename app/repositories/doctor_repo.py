from app.models import Doctor
from app.db import db


def get_all_doctors():
    return Doctor.query.all()
