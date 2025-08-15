import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class TestConfig(Config):
    uri = os.getenv("TEST_DATABASE_URL")
    if not uri:
        raise RuntimeError("Must set TEST_DATABASE_URL for tests.")
    SQLALCHEMY_DATABASE_URI = uri


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


def get_config(env_name):
    return {
        "dev": DevConfig,
        "test": TestConfig,
        "prod": ProdConfig,
    }.get(env_name, DevConfig)
