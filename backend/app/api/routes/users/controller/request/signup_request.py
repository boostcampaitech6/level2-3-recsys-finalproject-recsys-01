import re

from pydantic import BaseModel, validator
from ......exception.users.signup_exeption import (
    UserSignUpInvalidLoginIdException, UserSignUpLoginIdMissningException,
    UserSignUpPasswordMissningException, UserSignUpInvalidPasswordException,
    UserSignUpNicknameMissningException, UserSignUpInvalidNicknameException,
    UserSignUpEmailMissningException, UserSignUpInvalidEmailException,
)

MINIMUM_LOGIN_ID_LENGTH = 5
MINIMUM_PASSWORD_LENGTH = 8
MINIMUM_FAVOR_RECIPE_COUNT = 10

class SignupRequest(BaseModel):
    login_id: str
    password: str
    nickname: str
    email: str

    @validator('login_id')
    def validate_login_id(cls, login_id: str):
        if not login_id.strip():
            raise UserSignUpLoginIdMissningException(f"로그인 ID는 필수 입력입니다.")
        if len(login_id) < MINIMUM_LOGIN_ID_LENGTH:
            raise UserSignUpInvalidLoginIdException(f"로그인 ID는 최소 {MINIMUM_LOGIN_ID_LENGTH} 자리 이상이어야 합니다: {len(login_id)}")
    
    @validator('password')
    def validate_password(cls, password: str):
        if not password.strip():
            raise UserSignUpPasswordMissningException(f"비밀번호는 필수 입력입니다.")
        if len(password) < MINIMUM_PASSWORD_LENGTH:
            raise UserSignUpInvalidPasswordException(f"비밀번호는 최소 {MINIMUM_PASSWORD_LENGTH} 자리 이상이어야 합니다: {len(password)}")
        
    @validator('nickname')
    def validate_nickname(cls, nickname: str):
        if not nickname.strip():
            raise UserSignUpNicknameMissningException(f"닉네임은 필수 입력입니다.")
    
    @validator('email')
    def validate_email(cls, email: str):
        if not email.strip():
            raise UserSignUpEmailMissningException(f"이메일은 필수 입력입니다.")
        if not cls._valid_email(email):
            raise UserSignUpInvalidEmailException(f"이메일 형식에 맞지 않습니다: {email}")
    
    @staticmethod
    def _valid_email(email: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)


class LoginRequest(BaseModel):
    login_id: str
    password: str

    @validator('login_id')
    def validate_login_id(cls, login_id: str):
        if not login_id.strip():
            raise UserSignUpLoginIdMissningException(f"로그인 ID는 필수 입력입니다.")
        if len(login_id) < MINIMUM_LOGIN_ID_LENGTH:
            raise UserSignUpInvalidLoginIdException(f"로그인 ID는 최소 {MINIMUM_LOGIN_ID_LENGTH} 자리 이상이어야 합니다: {len(login_id)}")
    
    @validator('password')
    def validate_password(cls, password: str):
        if not password.strip():
            raise UserSignUpPasswordMissningException(f"비밀번호는 필수 입력입니다.")
        if len(password) < MINIMUM_PASSWORD_LENGTH:
            raise UserSignUpInvalidPasswordException(f"비밀번호는 최소 {MINIMUM_PASSWORD_LENGTH} 자리 이상이어야 합니다: {len(password)}")


class UserFavorRecipesRequest(BaseModel):
    recipes: list[str]

    @validator('recipes')
    def validate_login_id(cls, recipes: list[str]):
        if len(recipes) < MINIMUM_FAVOR_RECIPE_COUNT:
            raise UserSignUpInvalidLoginIdException(f"좋아하는 레시피는 최소 {MINIMUM_FAVOR_RECIPE_COUNT} 개 이상이어야 합니다: {len(recipes)}")
