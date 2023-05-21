from os import getenv

SQLALCHEMY_DATABASE_URI = getenv(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql+pg8000://lis:pass@localhost:5432/shop"
)

class Config:
    DEBUG = False
    TESTING = False
    ENV = ""
    SECRET_KEY="qwerty"
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_ECHO = False
    # USER_ENABLE_EMAIL = False

class ProductionConfig(Config):
    ENV = "production"

class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    SQLALCHEMY_ECHO = True