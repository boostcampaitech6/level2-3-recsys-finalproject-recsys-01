from typing import Optional
from pydantic import BaseModel

class UserSignupDTO(BaseModel):
    _id: Optional[str]
    login_id: str
    password: str
    nickname: str
    email: str

class UserLoginDTO(BaseModel):
    _id: Optional[str]
    login_id: str
    password: str