from flask import g, current_app, request
from aura.blueprints.auth_blueprint import auth
from aura.blueprints.common import ERROR, build_response

def register_common():
    @current_app.before_request
    def get_arguments():
        if request.method == 'POST':
            try:
                data = request.get_json()
            except TypeError:
                data = {}
            g.data = data

    @current_app.errorhandler
    def handle_unhandled(er):
        return build_response(ERROR, str(er))

    
def register_blueprints():
    current_app.register_blueprint(auth)
