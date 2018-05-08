from flask import g, current_app
from flask_sqlalchemy import SQLAlchemy


def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy(current_app)
    return g.db


def init_db():
    from flask_migrate import Migrate, upgrade
    Migrate(current_app, get_db())
    upgrade()
