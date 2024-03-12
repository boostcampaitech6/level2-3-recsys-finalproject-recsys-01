from ..repository.user_repository import UserRepository
from ..dto.user_dto import (
    UserSignupDTO, UserLoginDTO,
)
from ..controller.request.signup_request import UserFavorRecipesRequest

class UserService:
    def __init__(self, user_repository):
        self.repository: UserRepository = user_repository

    def sign_up(self, sign_up_request: UserSignupDTO) -> UserSignupDTO:
        return None
    
    def is_login_id_usable(self, login_id: str) -> bool:
        return False
    
    def is_nickname_usable(self, nickname: str) -> bool:
        return False
    
    def favor_recipes(self, page_num: int) -> list:
        return list()
    
    def save_favor_recipes(self, login_id: str, request: UserFavorRecipesRequest) -> None:
        return None
