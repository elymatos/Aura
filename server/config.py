import os

SQLALCHEMY_TRACK_MODIFICATIONS = False
HOST = os.getenv("AURA_HOST", '0.0.0.0')
PORT = os.getenv("AURA_PORT", 9090)
ENV = os.getenv("AURA_ENV", "dev")

if os.getenv("AURA_ENV") == "prod":
    SECRET_KEY = os.getenv("AURA_SECRET")
    SQLALCHEMY_DATABASE_URI = os.getenv("AURA_DB")
else:
    SECRET_KEY = 'super-secret'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/aura'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.abspath("database.db"))
    DEBUG = True