import json
from flask import g
from flask_jwt_extended import create_access_token, create_refresh_token, fresh_jwt_required
from unittest.mock import patch, MagicMock
from aura.database import get_db

@patch('aura.blueprints.auth_blueprint.create_user')
def test_create_user(mock, client, app):
    # If user was not created, return a reason message
    mock.return_value = (False, "")
    failed = client.post('/create_user')
    assert failed.status_code == 200
    data = json.loads(failed.data)
    assert data['status'] == "fail"
    assert isinstance(data['message'], str)

    # If user was created, return access_token and refresh_token
    mock_user = MagicMock()
    mock_user.id = 1
    mock.return_value = (True, mock_user)
    accepted = client.post('/create_user')
    assert accepted.status_code == 200
    data = json.loads(accepted.data)
    assert data['status'] == 'success'
    assert isinstance(data['data']['access_token'], str)
    assert isinstance(data['data']['refresh_token'], str)    


@patch('aura.blueprints.auth_blueprint.retrieve_user')
def test_login(mock, client, app):
    # If failed credentials, return error
    mock.return_value = (False, "")
    failed = client.post('/login')
    assert failed.status_code == 200
    data = json.loads(failed.data)
    assert data['status'] == "fail"
    assert isinstance(data['message'], str)

    # If successful login, return tokens
    mock_user = MagicMock()
    mock_user.id = 1
    mock.return_value = (True, mock_user)
    accepted = client.post('/login')
    assert accepted.status_code == 200
    data = json.loads(accepted.data)
    assert data['status'] == 'success'
    assert isinstance(data['data']['access_token'], str)
    assert isinstance(data['data']['refresh_token'], str)


def test_refresh(client, app):
    with app.app_context():
        refresh_token = create_refresh_token(1)

    # Returns 401 Unauthorized if no token is provided
    res = client.post('/refresh')
    assert res.status_code == 401

    # Returns 422 Unprocessable if invalid Bearer is provided
    headers = {'Authorization': 'Bearer foobar'}
    res = client.post('/refresh', headers=headers)
    assert res.status_code == 422

    # Returns new access_token if refresh_token is provided
    headers = {
        'Authorization': 'Bearer {}'.format(refresh_token)
    }
    res = client.post('/refresh', headers=headers)
    assert res.status_code == 200
    assert isinstance(json.loads(res.data)['access_token'], str)


@patch('aura.blueprints.auth_blueprint.retrieve_user')
def test_fresh_login(mock, client, app):
    #Invalid login returns fail
    mock.return_value = (False, "")
    res = client.post('/fresh_login')
    data = json.loads(res.data)
    assert data['status'] == "fail"
    assert isinstance(data['message'], str)

    #Valid login returns fresh access token. How to test freshness?
    mock_user = MagicMock()
    mock_user.id = 1
    mock.return_value = (True, mock_user)
    res = client.post('/fresh_login')
    data = json.loads(res.data)
    assert data['status'] == "success"
    assert isinstance(data['data']['access_token'], str)

"""
@patch('aura.blueprints.auth_blueprint.update_password')
def test_update_password(mock, client, app):
    #Invalid token returns unauthorized
    res = client.post('/update_password')
    assert res.status_code == 401

    #Failure on update password notifies user
    with app.app_context():
        #g.data = {'new_password':''}
        fresh_token = create_access_token(identity=1, fresh=True)
    headers = {
        'Authorization': 'Bearer {}'.format(fresh_token)
    }
    mock.return_value = False, ""
    res = client.post('/update_password', headers=headers)
    data = json.loads(res.data)
    assert data['status'] == "fail"
    assert isinstance(data['data']['message'], str)

    #Sucessul update password returns success
    mock.return_value = True, None
    data = json.loads(res.data)
    assert data['status'] == "success"    
"""