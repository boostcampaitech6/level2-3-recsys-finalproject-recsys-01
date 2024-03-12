from fastapi import APIRouter, Query, Request, Response, status
from typing import Optional

import logging
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from .request.signup_request import SignupRequest, LoginRequest, UserFavorRecipesRequest
from .response.signup_response import SignupResponse, LoginResponse, FavorRecipesResponse
from ..service.user_service import UserService
from ..repository.user_repository import UserRepository, SessionRepository, FoodRepository
from ..dto.user_dto import UserSignupDTO, UserLoginDTO

class UserController:
    def __init__(self, user_service: UserService):
        self.service: UserService = user_service
    
    async def sign_up(self, signup_request: SignupRequest) -> SignupResponse:
        return SignupResponse(
            **dict(self.service.sign_up(
                UserSignupDTO(**dict(signup_request))
            ))
        )
    
    async def login(self, login_request: UserLoginDTO) -> LoginResponse:
        return LoginResponse(
            **dict(self.service.login(login_request))
        )
    
    async def is_login_id_usable(self, login_id: str) -> bool:
        return self.service.is_login_id_usable(login_id)
    
    async def is_nickname_usable(self, nickname: str) -> bool:
        return self.service.is_nickname_usable(nickname)
    
    async def favor_recipes(self, page_num: int) -> list:
        return self.service.favor_recipes(page_num)
    
    async def save_favor_recipes(self, login_id: str, request: UserFavorRecipesRequest) -> None:
        return self.service.save_favor_recipes(login_id, request)


user_controller = UserController(UserService(
    UserRepository(), SessionRepository(), FoodRepository()))
user_router = APIRouter()

class Request(BaseModel):
    login_id: str
    password: str
    nickname: str
    email: str
    
@user_router.post('/api/users')
async def sign_up(request: SignupRequest) -> JSONResponse:
    # logging.info(request)
    response_body = await user_controller.sign_up(UserSignupDTO(
        login_id=request.login_id,
        password=request.password,
        nickname=request.nickname,
        email=request.email))
    return JSONResponse(content=response_body.model_dump(), status_code=status.HTTP_200_OK)

@user_router.post('/api/users/auth')
async def login(request: LoginRequest) -> Response:
    # logging.info(request)
    response_body = await user_controller.login(UserLoginDTO(
        login_id=request.login_id,
        password=request.password
    ))
    logging.debug(response_body)
    return JSONResponse(content=response_body.model_dump(), status_code=status.HTTP_200_OK)

# GET /api/users?login_id={login_id}
@user_router.get('/api/users')
async def validate_duplicate_info(
    login_id: Optional[str]=Query(None),
    nickname: Optional[str]=Query(None),
) -> Response:
    if login_id and login_id.strip():
        await user_controller.is_login_id_usable(login_id)
    if nickname and nickname.strip():
        await user_controller.is_nickname_usable(nickname)
    return Response(status_code=status.HTTP_200_OK)

# GET /api/foods?page={page_num}
@user_router.get('/api/users/foods')
async def favor_recipes(page_num: int=1) -> Response:
    response_body = await user_controller.favor_recipes(page_num)
    return JSONResponse(content=response_body, status_code=status.HTTP_200_OK)

# POST /api/users/{user_id}/foods
@user_router.post('/api/users/{user_id}/foods')
async def save_favor_recipes(user_id: str, request: UserFavorRecipesRequest) -> Response:
    await user_controller.save_favor_recipes(user_id, request)
    return Response(status_code=status.HTTP_200_OK)
