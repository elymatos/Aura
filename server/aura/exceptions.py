class ServiceError(ValueError): pass

class WrongPasswordError(ServiceError): pass

class DomainError(AttributeError, ValueError):

    def __init__(self, msg):
        super().__init__(msg)


class UserDomainError(DomainError): pass