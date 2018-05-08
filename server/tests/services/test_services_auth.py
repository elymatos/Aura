import pytest
from unittest.mock import patch
from aura.database import init_db, get_db
from aura.exceptions import ServiceError, DomainError, WrongPasswordError

@pytest.fixture
def app(app):
    init_db()
    

def test_retrieve_user(app):
    from aura.models import User
    from aura.services import retrieve_user
    with app.app_context():
        db = get_db()
        db.session.add(User(username='admin', password='admin'))
        db.session.commit()

        user = User.query.filter_by(username='admin').first()
        print("==")
        print(user)
        print("==")

        
        user = retrieve_user({'username':'admin', 'password': 'admin'})
        assert isinstance(user, User)
        assert user.username == 'admin'
        assert user.password_is('admin')
        
@pytest.mark.parametrize("data", [{'password':''}, {'username':''}])
def test_create_user_schema(app, data):
    from aura.services import create_user
    #Checks absence of keys: password, username
    with pytest.raises(ServiceError):    
        create_user(data)


@patch('aura.services.User')
def test_create_user_domain_error(mock, app):
    """
    If DomainError is thrown when creating user, catch it
    """
    from aura.services import create_user
    mock.side_effect = DomainError
    with pytest.raises(DomainError):
        create_user({'username': '', 'password':''})       


def test_create_user(app):
    from aura.services import create_user
    from aura.models import User
    user = create_user({'username': 'user', 'password':'hunter2'})
    assert isinstance(user, User)
    assert user.id is not None
    assert isinstance(User.query.filter_by(username='user').one(), User)
    

@pytest.mark.parametrize("data", [{'password':''}, {'username':''}])
def test_retrieve_user_schema(app, data):
    from aura.services import retrieve_user
    #Checks absence of keys: password, username
    with pytest.raises(ServiceError):    
        retrieve_user(data)


def test_retrieve_user_invalid_credentials(app):
    from aura.models import User
    db = get_db()
    db.session.add(User(username='admin', password='admin'))
    db.session.commit()

    from aura.services import retrieve_user
    #Non existing user
    with pytest.raises(ServiceError):
        retrieve_user({'username':'xxxx', 'password': 'xxxx'})
    #Wrong password still raises Service error
    with pytest.raises(ServiceError):
        retrieve_user({'username':'admin', 'password': 'xxxx'})

    