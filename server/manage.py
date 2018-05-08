import os
import click
import io
from contextlib import redirect_stdout
from flask import current_app
from flask_migrate import Migrate, upgrade
from aura.database import get_db


def register_cli():
    with current_app.app_context():
        migrate = Migrate(current_app, get_db())

        @current_app.cli.command()
        def sql():
            base_dir = os.path.abspath("aura/database")
            uri = current_app.config['SQLALCHEMY_DATABASE_URI']
            if uri.startswith('postgresql'):
                out = os.path.join(base_dir, "pg.sql")
            elif uri.startswith('sqlite'):
                out = os.path.join(base_dir, "sqlite.sql")
            else:
                raise ValueError("Unknown database URI: {}".format(uri))
            # https://stackoverflow.com/a/40984270/8188975
            data = io.StringIO()
            with redirect_stdout(data):
                upgrade(sql=True)
            with open(out, 'w') as f:
                f.write(data.getvalue())
            print("Written to: {}".format(out))
