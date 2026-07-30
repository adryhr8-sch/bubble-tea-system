class BaseException(Exception):
    pass

class DuplicateEmailError(BaseException):
    pass

class InvalidPasswordError(BaseException):
    pass

class DuplicateTeaError(BaseException):
    pass

class InsufficientStockError(BaseException):
    pass

class InvalidOrderError(BaseException):
    pass

class PaymentRejectedError(BaseException):
    pass