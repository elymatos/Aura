from sqlalchemy.ext.hybrid import hybrid_property
from base64 import b64encode
from hashlib import sha256
from datetime import datetime
import bcrypt
from aura.strings import USERNAME_EMPTY, USERNAME_LENGTH_FAIL, PASSWORD_TOO_SHORT
from aura.constants import PASSWORD_MIN_LENGTH, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH
from aura.exceptions import UserDomainError
from aura.database import get_db

db = get_db()


roles_users = db.Table('roles_users', db.metadata,
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id'), primary_key=True),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'), primary_key=True)
        )


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column('id', db.Integer(), db.Sequence('role_seq_id'), primary_key=True)
    name = db.Column('name', db.String(), unique=True, nullable=False)
    description = db.Column('description', db.String())
    
    def __init__(self, id=None, name=None, description=None):
        self.id = id
        self.name = name
        self.description = description

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer(), db.Sequence('user_seq_id'), primary_key=True)
    _username = db.Column('username', db.String(), unique=True, nullable=False)
    _password = db.Column('password', db.String(), nullable=False)
    
    active = db.Column('active', db.Boolean(), default=True)
    
    roles = db.relationship('Role', secondary=roles_users,
                        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.active = True
        self.created_at = datetime.now()
        self.roles = []
    
    @hybrid_property
    def username(self): return self._username  # pylint: disable=E0202

    @hybrid_property
    def password(self): return self._password  # pylint: disable=E0202
        
    @username.setter
    def username(self, name):
        s = len(name)
        if not name:
            raise UserDomainError(USERNAME_EMPTY)
        if not USERNAME_MIN_LENGTH < len(name) < USERNAME_MAX_LENGTH: 
            raise UserDomainError(USERNAME_LENGTH_FAIL)
        self._username = name
        
    @password.setter
    def password(self, pw):
        if not pw or len(pw) < PASSWORD_MIN_LENGTH:
            raise UserDomainError(PASSWORD_TOO_SHORT)
        pw = pw.encode('utf-8')
        if len(pw) > 72:
            pw = b64encode(sha256().digest())
        self._password = bcrypt.hashpw(pw, bcrypt.gensalt())
        
    def password_is(self, pw):
        pw = pw.encode('utf-8')
        if len(pw) > 72:
            pw = b64encode(sha256(pw).digest())
        return bcrypt.checkpw(pw, self.password)


