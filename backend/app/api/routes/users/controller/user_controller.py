from fastapi import APIRouter, Request, Response, status

from .request.signup_request import SignupRequest, LoginRequest, UserFavorRecipesRequest
from .response.signup_response import SignupResponse, LoginResponse, FavorRecipesResponse
from ..service.user_service import UserService
from ..dto.user_dto import UserSignupDTO, UserLoginDTO


class UserController:
    def __init__(self, user_service: UserService):
        self.service: UserService = user_service
    
    def sign_up(self, signup_request: SignupRequest) -> SignupResponse:
        return SignupResponse(
            **self.service.signup(
                UserSignupDTO(**signup_request)
            )
        )
    
    def is_login_id_usable(self, login_id: str) -> bool:
        return self.service.is_login_id_usable(login_id)
    
    def is_nickname_usable(self, nickname: str) -> bool:
        return self.service.is_nickname_usable(nickname)
    
    def favor_recipes(self, page_num: int) -> list:
        return self.service.favor_recipes(page_num)
    
    def save_favor_recipes(self, login_id: str, request: UserFavorRecipesRequest) -> None:
        return self.service.save_favor_recipes(login_id, request)


user_controller = UserController(UserService())
router = APIRouter('/api/users')

@router.post()
async def sign_up(request: SignupRequest) -> Response:
    response_body = await user_controller.sign_up(UserSignupDTO(
        login_id=request.login_id,
        password=request.password,
        nickname=request.nickname,
        email=request.email))
    return Response(content=SignupResponse(**response_body), status_code=status.HTTP_200_OK)

@router.post('/auth')
async def login(request: LoginRequest) -> Response:
    response_body = await user_controller.login(UserLoginDTO(
        login_id=request.login_id,
        password=request.password
    ))
    return Response(content=LoginResponse(**response_body), status_code=status.HTTP_200_OK)

# GET /api/users?login_id={login_id}
@router.get()
async def is_usable_login_id(login_id: str) -> Response:
    await user_controller.is_login_id_usable(login_id)
    return Response(status_code=status.HTTP_200_OK)

# GET /api/users?nickname={nickname}
@router.get('/')
async def is_usable_nickname(nickname: str) -> Response:
    await user_controller.is_nickname_usable(nickname)
    return Response(status_code=status.HTTP_200_OK)

# GET /api/foods?page={page_num}
@router.get('/')
async def favor_recipes(page_num: int=1) -> Response:
    response_body = await user_controller.favor_recipes(page_num)
    return Response(content=FavorRecipesResponse(**response_body), status_code=status.HTTP_200_OK)

# POST /api/users/{user_id}/foods
@router.post('/{user_id}/foods')
async def save_favor_recipes(user_id: str, request: UserFavorRecipesRequest) -> Response:
    await user_controller.save_favor_recipes(user_id, request)
    return Response(status_code=status.HTTP_200_OK)
