import uuid
from datetime import datetime, timedelta

from ..entity.user import User
from ..repository.user_repository import UserRepository, SessionRepository, FoodRepository
from ..dto.user_dto import (
    UserSignupDTO, UserLoginDTO,
)
from ..controller.request.signup_request import UserFavorRecipesRequest

class UserService:
    def __init__(self, user_repository :UserRepository, session_repository: SessionRepository, food_repository: FoodRepository):
        self.user_repository: UserRepository = user_repository
        self.session_repository: SessionRepository = session_repository
        self.food_repository: FoodRepository = food_repository

    def sign_up(self, sign_up_request: UserSignupDTO) -> UserSignupDTO:
        return self.user_repository.insert_one(sign_up_request)
    
    def login(self, login_request: UserLoginDTO) -> UserLoginDTO:
        user = User(**dict(self.user_repository.find_one({'login_id': login_request.login_id, 'password': login_request.password})))
        if user is None:
            raise ValueError("아이디와 비밀번호가 일치하지 않습니다.")
        
        token = str(uuid.uuid4())
        expire_date = datetime.utcnow() + timedelta(seconds=30 * 60)
        return self.session_repository.insert_one(login_id=login_request.login_id, token=token, expire_date=expire_date)
    
    def is_login_id_usable(self, login_id: str) -> bool:
        if self.user_repository.find_one({'login_id': login_id}) is not None:
            raise ValueError(f"중복되는 아이디 입니다: {login_id}")
        return True
    
    def is_nickname_usable(self, nickname: str) -> bool:
        if self.user_repository.find_one({'nickname': nickname}) is not None:
            raise ValueError(f"중복되는 닉네임 입니다: {nickname}")
        return True
    
    def favor_recipes(self, page_num: int) -> list:
        return self.food_repository.find_foods(page_num)
    
    def save_favor_recipes(self, login_id: str, request: UserFavorRecipesRequest) -> None:
        self.user_repository.update_food(login_id, request.recipes)
