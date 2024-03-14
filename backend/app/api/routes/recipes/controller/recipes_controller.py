from fastapi import APIRouter
from ..service.recipes_service import *
from ..dto.get_recipes_reponse_list import GetRecipesReponseList


recipes_router = APIRouter()

@recipes_router.get(
    "/users/{user_id}/recipes/cooked", 
    response_description="유저가 요리한 레시피 목록"
    )
def get_user_cooked_recipes_by_page(user_id: str, page_num: int = 0):
    # user_id로 유저 조회
    user = get_user_by_user_id(user_id)
    # user로 유저가 요리한 레시피 id 리스트 조회
    user_cooked_recipes_id = get_user_cooked_recipes_id_by_user(user)
    # 레시피 id 리스트로 각 레시피의 정보 조회
    recipes = get_recipes_by_recipes_id(user_cooked_recipes_id)
    # 레시피로 Ingredients 리스트 조회
    ingredients_list = get_ingredients_list_by_recipes(recipes)
    return GetRecipesReponseList(recipes, ingredients_list)


@recipes_router.get(
    "/users/{user_id}/recipes/recommended", 
    response_description="유저가 추천받은 레시피 목록"
    )
def get_user_recommended_recipes_by_page(user_id: str, page_num: int = 0):
    # user_id로 유저가 추천 받은 레시피 id 리스트 조회
    user = get_user_by_user_id(user_id)
    user_cooked_recipes_id = get_user_cooked_recipes_id_by_user(user)
    user_recommended_recipes_id = get_user_recommended_recipes_id_by_user(user)
    # 레시피 id 리스트로 각 레시피의 정보 조회
    recipes = get_recipes_by_recipes_id(user_cooked_recipes_id + user_recommended_recipes_id)
    # 레시피로 Ingredients 리스트 조회
    ingredients_list = get_ingredients_list_by_recipes(recipes)
    # 유저가 요리한 요리 표시를 위한 user_cooked_recipes_id 함께 넘기기
    return GetRecipesReponseList(recipes, ingredients_list, user_cooked_recipes_id)