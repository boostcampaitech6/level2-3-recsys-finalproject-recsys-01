from pydantic import BaseModel

class User(BaseModel):
    login_id: str
    password: str
    nickname: str
    email: str