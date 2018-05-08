import os
from flask import Flask, current_app, request, g
from flask_migrate import Migrate


def create_app(config=None):
    app = Flask(__name__)
    with app.app_context():
        if config is not None:
            app.config.update(config)
        else:
            app.config.from_pyfile('../config.py', silent=True)

        #try:
        #    os.makedirs(app.instance_path)
        #except OSError:
        #    pass
        #from aura.database import get_db, init_db
        #migrate = Migrate(app, get_db())

        from manage import register_cli
        register_cli()

        from flask_jwt_extended import JWTManager
        JWTManager(current_app)
        
        from aura.blueprints import register_common, register_blueprints
        register_common()
        register_blueprints()
    return app
