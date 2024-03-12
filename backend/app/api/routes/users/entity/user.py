from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    _id: Optional[str]
    login_id: str
    password: str
    nickname: str
    email: str

class Session(BaseModel):
    _id: Optional[str]
    user_id: str