import os
import tempfile
import pytest
from aura import create_app
from aura.database import get_db

@pytest.fixture
def app(tmpdir):
    db_fd, db_path = tempfile.mkstemp(dir=str(tmpdir))
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': "sqlite:///" + db_path,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'secret-test'
    })
    app.app_context().push()
    yield app    
    os.close(db_fd)
    #os.unlink(db_path)


@pytest.fixture
def context(app):
    return app.test_request_context()


@pytest.fixture
def client(app):
    return app.test_client()

"""
class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post('/login', jsonify(username=username, password=password))


@pytest.fixture
def auth(client):
    return AuthActions(client)
"""