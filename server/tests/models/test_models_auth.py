import pytest
from unittest.mock import patch
from aura.exceptions import UserDomainError

@patch('aura.models.User.__init__')
@pytest.mark.parametrize("pw", ["", "aa"])
def test_password_failures(mock_user, pw, app):    
    mock_user.return_value = None
    from aura.models import User
    
    user = User()
    #Password empty, too short
    with pytest.raises(UserDomainError):
        user.password = pw
        

@patch('aura.models.User.__init__')
@pytest.mark.parametrize("name", ["", "aa", "a"*16])
def test_username_failures(mock_user, name, app):
    mock_user.return_value = None
    from aura.models import User
    user = User()
    #Username empty, too short, too long
    with pytest.raises(UserDomainError):            
        user.username = name
        

def test_constructor(app):
    from aura.models import User
    user = User(username="user", password="pass")
    assert user.username == "user"
    assert user.password_is("pass")


def test_hybrid_properties(app):
    from aura.models import User
    user = User(username="user", password="pass")
    assert user.username == user._username
    assert user.password == user._password


def test_setter_properties(app):
    from aura.models import User
    user = User(username="user", password="pass")    
    user.username = "other"
    assert user.username == "other"
    user.password = "otherpass"
    assert user.password_is("otherpass")

def test_password_encryption(app):
    from aura.models import User
    user = User("user", "pass")
    assert user.password != "pass"
    
