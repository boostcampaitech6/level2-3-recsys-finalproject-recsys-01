from fastapi import status, Request
from fastapi.responses import JSONResponse

from ...app import app
from .user_exception import UserException

@app.exception_handler(UserException)
async def custom_exception_handler(request : Request, exc: UserException):
    if isinstance(exc, UserSignUpLoginIdMissningException):
        status_code = status.HTTP_400_BAD_REQUEST
        content = {'message': exc.message}
    return JSONResponse(
        status_code=status_code,  # 예외에 따라 상태 코드를 조정할 수 있습니다.
        content=content
    )

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
