import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory_"


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


def get_config(env_name):
    return {
        "dev": DevConfig,
        "test": TestConfig,
        "prod": ProdConfig,
    }.get(env_name, DevConfig)
