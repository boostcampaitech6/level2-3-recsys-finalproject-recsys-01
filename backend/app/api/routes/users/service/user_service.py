from ..repository.user_repository import UserRepository
from ..dto.user_dto import (
    UserSignupDTO, UserLoginDTO,
)

class UserService:
    def __init__(self, user_repository):
        self.repository: UserRepository = user_repository

    # def sign_up(self, sign_up_request: UserSignupDTO) -> UserSignupDTO:
    #     return UserSignupDTO(**{
    #         '_id': '',
    #         'login_id': '',
    #         'password': '', 
    #     })