import pytest
import os
from sqlalchemy.orm import scoped_session, sessionmaker
from app import create_app
from app.db import db as _db
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("TEST_DATABASE_URL")
assert uri and uri.startswith(
    "postgresql://"
), "TEST_DATABASE_URL must be set to a Postgres URL for tests."


@pytest.fixture(scope="session")
def app():
    app = create_app("test")
    context = app.app_context()
    context.push()
    yield app
    context.pop()


@pytest.fixture(scope="session")
def db(app):
    _db.drop_all()
    _db.create_all()
    yield _db


@pytest.fixture(autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    _session = scoped_session(Session)

    db.session = _session

    try:
        yield _session
    finally:
        transaction.rollback()
        connection.close()
        _session.remove()


@pytest.fixture
def client(app):
    return app.test_client()


pytest_plugins = [
    "tests.fixtures.doctors",
]
