import base64
import os
from pathlib import Path
from typing import Type

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    # Случайный ключ для подписи данных
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')

    # For paginate
    ITEMS_PER_PAGE = 12

    # SQL settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # For PyJWT
    JWT_SECRET = '8wpJ0zgpEL'
    JWT_ALGORITHM = 'HS256'

    TOKEN_EXPIRE_MINUTES = 15
    TOKEN_EXPIRE_DAYS = 130

    PWD_HASH_SALT = base64.b64decode("project4")
    PWD_HASH_ITERATIONS = 100_000

    # For correct display of Cyrillic fonts
    JSON_AS_ASCII = False
    RESTX_JSON = {
        'ensure_ascii': False,
    }

    @staticmethod
    def init_app(app):
        pass


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + BASE_DIR.joinpath('project.db').as_posix()


class ProductionConfig(BaseConfig):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = "postgresql://psqluser:psqlpassword@psql/psql"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + BASE_DIR.joinpath('project.db').as_posix()


class ConfigFactory:
    flask_env = os.getenv('FLASK_ENV')

    @classmethod
    def get_config(cls) -> Type[BaseConfig]:
        if cls.flask_env == 'development':
            return DevelopmentConfig
        elif cls.flask_env == 'production':
            return ProductionConfig
        elif cls.flask_env == 'testing':
            return TestingConfig
        raise NotImplementedError


config = ConfigFactory.get_config()

if __name__ == "__main__":
    pass
