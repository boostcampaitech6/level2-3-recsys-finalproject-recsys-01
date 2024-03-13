from typing import List
from ..repository.recipes_repository import select_user_by_user_id, select_recipes_by_recipes_id, select_ingredients_by_ingredients_id
from ..entity.recipes import Recipes


def get_user_cooked_recipes(user_id: str) -> List[str]:
    user = select_user_by_user_id(user_id)
    user_cooked_recipes = user.get_feedback_history()
    return user_cooked_recipes


def get_recipes_by_recipes_id(recipes_id: List[str]) -> Recipes: 
    # 레시피 리스트 조회
    recipes = select_recipes_by_recipes_id(recipes_id)
    return recipes


def get_ingredients_collections_by_recipes(recipes: Recipes) -> List[Recipes]:
    # 레시피 별로 재료 리스트 조회: 
    # [Ingredients(ingredients: [Ingredient, Ingredient]), Ingredients(ingredients: [Ingredient, Ingredient])]
    ingredients_collection = [select_ingredients_by_ingredients_id(recipe.get_ingredients()) for recipe in recipes.get_recipes()]
    return ingredients_collection
    
    