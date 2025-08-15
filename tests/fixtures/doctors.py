import pytest
from tests.test_seed.seed_doctors import seed_doctors
from app.db import db
from app.models import Doctor


@pytest.fixture
def doctor():
    _doctor = Doctor(first_name="John", last_name="Doe", email="john.doe@example.com")
    db.session.add(_doctor)
    db.session.flush()
    return _doctor


@pytest.fixture
def seeded_doctors(session):
    return seed_doctors()
