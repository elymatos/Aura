from flask import Blueprint, json, jsonify, request, g, current_app
from flask_jwt_extended import (jwt_refresh_token_required, jwt_required, fresh_jwt_required, get_jwt_identity,
                                create_access_token, create_refresh_token)
from aura.services import create_user, retrieve_user, update_password
from aura.blueprints.common import build_response, FAIL, ERROR, SUCCESS
auth = Blueprint('auth', __name__)


@auth.route('/create_user', methods=['POST'])
def route_create_user():
    result, payload = create_user(g.data)
    print(result, payload)
    if result:
        response = {
            'access_token': create_access_token(identity=payload.id),
            'refresh_token': create_refresh_token(identity=payload.id)
        }
        return build_response(SUCCESS, response)
    else:
        return build_response(FAIL, str(payload))    


@auth.route('/login', methods=['POST'])
def route_login():
    result, payload = retrieve_user(g.data)
    if result:
        response = {
            'access_token': create_access_token(identity=payload.id),
            'refresh_token': create_refresh_token(identity=payload.id)
        }
        return build_response(SUCCESS, response)
    else:
        return build_response(FAIL, str(payload))


@auth.route('/heey', methods=['POST'])
@jwt_required
def heey():
    return jsonify(message="token accepted ;)", id=get_jwt_identity())


@auth.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    id = get_jwt_identity()
    new_token = create_access_token(identity=id, fresh=False)
    return jsonify(access_token=new_token), 200


@auth.route('/fresh_login', methods=['POST'])
def fresh_login():
    result, payload = retrieve_user(g.data)
    if result:
        new_token = create_access_token(identity=payload.id, fresh=True)
        return build_response(SUCCESS, {'access_token':new_token})
    else:
        return build_response(FAIL, str(payload))


@auth.route('/update_password', methods=['POST'])
@fresh_jwt_required
def change_password():
    id = get_jwt_identity()
    update_password(id, g.data['new_password'])