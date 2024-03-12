from fastapi import APIRouter, Request, Response, status

from .request.signup_request import SignupRequest, LoginRequest
from .response.signup_response import SignupResponse
from ..service.user_service import UserService
from ..dto.user_dto import UserSignupDTO


class UserController:
    def __init__(self, user_service: UserService):
        self.service: UserService = user_service
    
    def sign_up(self, signup_request: SignupRequest) -> SignupResponse:
        return SignupResponse(
            **self.service.signup(
                UserSignupDTO(**signup_request)
            )
        )

user_controller = UserController(UserService())
router = APIRouter('/api/users')

@router.post('/')
async def sign_up(request: SignupRequest) -> Response:
    # response_body = await user_controller.sign_up(UserSignupDTO(
    #     login_id=request.login_id,
    #     password=request.password,
    #     nickname=request.nickname,
    #     email=request.email))
    # return Response(content=SignupResponse(**response_body), status_code=status.HTTP_200_OK)
    pass

@router.post('/auth')
async def login(request: LoginRequest) -> Response:
    pass

# GET /api/users?login_id={login_id}
@router.get('/')
async def is_usable_login_id(login_id: str) -> Response:
    pass

# GET /api/users?nickname={nickname}
@router.get('/')
async def is_usable_nickname(nickname: str) -> Response:
    pass

# GET /api/foods?page={page_num}
@router.get('/')
async def favor_recipes(page_num: int=1) -> Response:
    pass

# POST /api/users/{user_id}/foods
@router.post('/{user_id}/foods')
async def save_favor_recipes(user_id: str, UserFavorRequest) -> Response:
    pass