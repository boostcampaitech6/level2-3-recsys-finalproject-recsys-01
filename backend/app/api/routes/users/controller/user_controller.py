from fastapi import APIRouter, Query, Response, status
from typing import Optional
from datetime import datetime as dt

import logging
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from app.api.routes.recipes.entity.recipes import Recipes
from .request.signup_request import SignupRequest, LoginRequest, UserFavorRecipesRequest
from .response.signup_response import SignupResponse, LoginResponse, FavorRecipesResponse
from ..service.user_service import UserService
from app.api.routes.recipes.service.recipes_service import RecipesService
from ..repository.user_repository import (
    UserRepository, SessionRepository, FoodRepository, RecommendationRepository, BasketRepository
)
from ..dto.user_dto import UserSignupDTO, UserLoginDTO

class UserController:
    def __init__(self, user_service: UserService, recipe_service: RecipesService):
        self.user_service: UserService = user_service
        self.recipe_service: RecipesService = recipe_service
    
    async def sign_up(self, signup_request: SignupRequest) -> SignupResponse:
        self.user_service.is_login_id_usable(signup_request.login_id)
        self.user_service.is_nickname_usable(signup_request.nickname)
        return SignupResponse(
            **dict(self.user_service.sign_up(
                UserSignupDTO(**dict(signup_request))
            ))
        )
    
    async def login(self, login_request: UserLoginDTO) -> LoginResponse:
        return LoginResponse(
            **dict(self.user_service.login(login_request))
        )
    
    async def is_login_id_usable(self, login_id: str) -> bool:
        return self.user_service.is_login_id_usable(login_id)
    
    async def is_nickname_usable(self, nickname: str) -> bool:
        return self.user_service.is_nickname_usable(nickname)
    
    async def favor_recipes(self, page_num: int) -> list:
        foods, has_next = self.user_service.favor_recipes(page_num)
        return {
            'foods': foods,
            'next_page_url': f'/api/users/foods?page_num={page_num+1}' if has_next else ''
        }
    
    async def save_favor_recipes(self, login_id: str, request: UserFavorRecipesRequest) -> None:
        return self.user_service.save_favor_recipes(login_id, request)
    
    async def recommended_basket(self, user_id: str, price: int):
        # top k recipes id 가져옴
        top_k_recipes = self.user_service.top_k_recipes(user_id, price)

        # recipe 정보 가져오기
        recipe_infos = self.recipe_service.get_recipes_by_recipes_id(top_k_recipes)

        # ingredient 정보 가져오기
        price_infos = self.recipe_service.get_prices_by_ingredients_id(recipe_infos.get_total_ingredients_set())

        # 장바구니 추천
        recipes = recipe_infos.get_recipes()
        recipes = {recipe.get_id(): recipe.get_ingredients() for recipe in recipes}

        recommended_basket = self.user_service.recommended_basket(recipes, price_infos, price)

        # 추천 장바구니 결과 저장
        self.user_service.save_basket(user_id, price, dt.now(), recommended_basket)

        recommended_basket = self._basket_with_infos(recommended_basket, recipe_infos)

        return recommended_basket
    
    def _basket_with_infos(self, recommended_basket: dict, recipe_infos: Recipes):
        logging.debug('recommended_basket', recommended_basket)
        # logging.debug(recipe_infos)

        recipe_info_list = [recipe.as_basket_form() for recipe in recipe_infos.get_recipes() if recipe.get_id() in recommended_basket['recipe_list']]
        # logging.debug('Basket Form', recipe_info_list)

        total_ingredients = self.recipe_service.get_ingredients_by_ingredients_id(recipe_infos.get_total_ingredients_set())
        ingredient_info_list = [ingredient.as_basket_form() for ingredient in total_ingredients if ingredient.get_id() in recommended_basket['ingredient_list']]
        # logging.debug('Ingredient Basket Form', ingredient_info_list)

        basket_with_infos = {
            'basket_price': 0,
            'ingredient_list': ingredient_info_list,
            'recipe_list': recipe_info_list,
        }
        return basket_with_infos


user_controller = UserController(
    UserService(
        UserRepository(),
        SessionRepository(),
        FoodRepository(),
        RecommendationRepository(),
        BasketRepository()),
    RecipesService()
)
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

@user_router.post('/api/users/auths')
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
    logging.debug(response_body)
    return JSONResponse(content=response_body, status_code=status.HTTP_200_OK)

# POST /api/users/{user_id}/foods
@user_router.post('/api/users/{user_id}/foods')
async def save_favor_recipes(user_id: str, request: UserFavorRecipesRequest) -> Response:
    await user_controller.save_favor_recipes(user_id, request)
    return Response(status_code=status.HTTP_200_OK)

@user_router.post('/api/users/{user_id}/recommendations')
async def get_recommendation(user_id: str, price: int) -> JSONResponse:
    '''{
        "basket_price": 46000,
        "ingredient_list": [
            {
                "ingredient_id": 10,
                "ingredient_name": "브로콜리",
                "ingredient_amount": 1,
                "ingredient_unit": "kg",
                "ingredient_price": 4680,
                "img_link": "https://health.chosun.com/site/data/img_dir/2024/01/19/2024011902009_0.jpg",
                "market_url":
                "https://www.coupang.com/vp/products/4874444452?itemId=6339533080&vendorItemId=73634892616&pickType=COU_PICK&q=%EB%B8%8C%EB%A1%9C%EC%BD%9C%EB%A6%AC&itemsCount=36&searchId=891d0b69dc8f452daf392e3db2482732&rank=1&isAddedCart="
            },...
        ],
        "recipe_list": [
            {
                "recipe_id": 1,
                "recipe_name": "어묵 김말이",
                "ingredient": [
                    {"ingredient_id": "1",
                    "ingredient_name": "어묵"},
                    {"ingredient_id": "2",
                    "ingredient_name": "김말이"}
                ],
                "recipe_img_url": "https://recipe1.ezmember.co.kr/cache/recipe/2015/05/18/1fb83f8578488ba482ad400e3b62df49.jpg",
                "recipe_url": "https://www.10000recipe.com/recipe/128671"
            },...
        ]
    }'''
    response_body = await user_controller.recommended_basket(user_id, price)
    return JSONResponse(content=response_body, status_code=status.HTTP_200_OK)
