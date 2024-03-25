from .user_exception import UserException

class UserSingUpException(UserException):
    def __init__(self, message):
        super().__init__(message)

class UserSignUpLoginIdMissningException(UserSingUpException):
    def __init__(self, message):
        super().__init__(message)

class UserSignUpPasswordMissningException(UserSingUpException):
    def __init__(self, message):
        super().__init__(message)

class UserSignUpNicknameMissningException(UserSingUpException):
    def __init__(self, message):
        super().__init__(message)

class UserSignUpEmailMissningException(UserSingUpException):
    def __init__(self, message):
        super().__init__(message)

class UserSignUpEmailMissningException(UserSingUpException):
    def __init__(self, message):
        super().__init__(message)

class UserSignUpInvalidLoginIdException(UserSingUpException):
    def __init__(self, message):
        super().__init__(message)

class UserSignUpInvalidPasswordException(UserSingUpException):
    def __init__(self, message):
        super().__init__(message)

class UserSignUpInvalidNicknameException(UserSingUpException):
    def __init__(self, message):
        super().__init__(message)

class UserSignUpInvalidEmailException(UserSingUpException):
    def __init__(self, message):
        super().__init__(message)

class UserSignUpLoginIdDuplicateException(UserSingUpException):
    def __init__(self, message):
        super().__init__(message)

class UserSignUpNicknameDuplicateException(UserSingUpException):
    def __init__(self, message):
        super().__init__(message)
