from schema import Schema, And, SchemaError
from aura.database import get_db
from aura.models import User
from aura.strings import USERNAME_OR_PASSWORD_INVALID
from aura.exceptions import ServiceError, DomainError, WrongPasswordError
db = get_db()

def validate(schema, data):
    try:
        return schema.validate(data)
    except SchemaError:
        raise ServiceError("""Invalid data provided. Schema required: {}""".format(str(schema)))


def create_user(data):
    data = validate(Schema({
            'username': str,
            'password': str
        }, ignore_extra_keys=True), data)    
    
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return user

    
def retrieve_user(data):
    data = validate(Schema({
        'username': str,
        'password': str
    }, ignore_extra_keys=True), data)
    try:
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            raise ServiceError()
        if not user.password_is(data['password']):
            raise WrongPasswordError()
        return user
    except WrongPasswordError:
        #Particular treatment of WrongPassword: lock out?
        #raise generic ServiceError though
        raise ServiceError
        

def update_password(user_id, new_password):
    try:
        user = User.query.get(user_id)
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        return True, None
    except Exception as e:
        return False, e
