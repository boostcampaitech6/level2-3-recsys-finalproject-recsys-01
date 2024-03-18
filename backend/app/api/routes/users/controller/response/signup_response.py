from pydantic import BaseModel

class SignupResponse(BaseModel):
    _id: str
    login_id: str
    password: str
    nickname: str
    email: str

class LoginResponse(BaseModel):
    token: str
    login_id: str
    password: str

class FavorRecipesResponse(BaseModel):
    recipes: list