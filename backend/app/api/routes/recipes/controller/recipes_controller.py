from fastapi import APIRouter, Response, HTTPException
from ..service.recipes_service import RecipesService
from ..dto.get_recipes_reponse_list import GetRecipesReponseList
from ..dto.recipe_status_upadate_request import RecipeStatusUpadateRequest


recipes_router = APIRouter()
recipes_service = RecipesService()

@recipes_router.get(
    "/users/{user_id}/recipes/cooked", 
    response_description="유저가 요리한 레시피 목록"
    )
def get_user_cooked_recipes_by_page(user_id: str, page_num: int = 0):
    # user_id로 유저 조회
    user = recipes_service.get_user_by_user_id(user_id)
    # user로 유저가 요리한 레시피 id 리스트 조회
    user_cooked_recipes_id = recipes_service.get_user_cooked_recipes_id_by_user(user)
    # 레시피 id 리스트로 각 레시피의 정보 조회
    recipes = recipes_service.get_recipes_by_recipes_id(user_cooked_recipes_id)
    # 레시피로 Ingredients 리스트 조회
    ingredients_list = recipes_service.get_ingredients_list_by_recipes(recipes)
    return GetRecipesReponseList(recipes, ingredients_list)


@recipes_router.get(
    "/users/{user_id}/recipes/recommended", 
    response_description="유저가 추천받은 레시피 목록"
    )
def get_user_recommended_recipes_by_page(user_id: str, page_num: int = 0):
    # user_id로 유저가 추천 받은 레시피 id 리스트 조회
    user = recipes_service.get_user_by_user_id(user_id)
    user_cooked_recipes_id = recipes_service.get_user_cooked_recipes_id_by_user(user)
    user_recommended_recipes_id = recipes_service.get_user_recommended_recipes_id_by_user(user)
    # 레시피 id 리스트로 각 레시피의 정보 조회
    recipes_id = user_cooked_recipes_id + user_recommended_recipes_id
    recipes = recipes_service.get_recipes_by_recipes_id(recipes_id)
    # 레시피로 Ingredients 리스트 조회
    ingredients_list = recipes_service.get_ingredients_list_by_recipes(recipes)
    # 유저가 요리한 요리 표시를 위한 user_cooked_recipes_id 함께 넘기기
    return GetRecipesReponseList(recipes, ingredients_list, user_cooked_recipes_id)


@recipes_router.patch("/users/{user_id}/recipes/{recipes_id}/feedback")
def update_user_recipes_status__by_feedback(user_id: str, recipes_id: str, request: RecipeStatusUpadateRequest):
    update_result = recipes_service.update_cooked_recipes(user_id, recipes_id, request.feedback)
    if update_result:
        return Response(status_code=200)
    raise HTTPException(status_code=404, detail="User not found")

