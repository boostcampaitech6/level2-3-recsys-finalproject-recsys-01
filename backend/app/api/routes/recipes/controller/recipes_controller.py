from fastapi import APIRouter
from ..service.recipes_service import get_user_cooked_recipes, get_recipes_by_recipes_id, get_ingredients_list_by_recipes
from ..dto.get_recipes_reponse_list import GetRecipesReponseList

recipes_router = APIRouter()

@recipes_router.get(
    "/users/{user_id}/recipes/cooked", 
    response_description="유저가 요리한 레시피 목록",
    response_model=GetRecipesReponseList
    )
def get_user_cooked_recipes_by_page(user_id: str, page_num: int = 0):
    # user_id로 유저가 요리한 레시피 id 리스트 조회
    user_cooked_recipes_id = get_user_cooked_recipes(user_id)
    # 레시피 id 리스트로 각 레시피의 정보 조회
    recipes = get_recipes_by_recipes_id(user_cooked_recipes_id)
    # 레시피로 Ingredients 리스트 조회
    ingredients_collection = get_ingredients_list_by_recipes(recipes)
    return GetRecipesReponseList(recipes, ingredients_collection)