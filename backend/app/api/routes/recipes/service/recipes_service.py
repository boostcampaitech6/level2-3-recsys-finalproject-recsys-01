from typing import List

from ..repository.recipes_repository import RecipesRepository
from ..entity.recipes import Recipes
from ..entity.ingredients import Ingredients
from ..entity.user import User


class RecipesService:
    def __init__(self, recipes_repository: RecipesRepository = None):
        self.recipes_repository = RecipesRepository()
        
    def get_user_by_user_id(self, user_id: str) -> User:
        user = self.recipes_repository.select_user_by_user_id(user_id)
        return user


    def get_user_cooked_recipes_id_by_user(self, user: User) -> List[str]:
        user_cooked_recipes_id = user.get_feedback_history()
        return user_cooked_recipes_id


    def get_user_recommended_recipes_id_by_user(self, user: User) -> List[str]:
        user_recommended_recipes_id = user.get_recommend_history_by_basket()
        return user_recommended_recipes_id


    def get_recipes_by_recipes_id(self, recipes_id: List[str]) -> Recipes: 
        # 레시피 리스트 조회
        return self.recipes_repository.select_recipes_by_recipes_id(recipes_id)


    def get_ingredients_list_by_recipes(self, recipes: Recipes) -> List[Ingredients]:
        # 레시피 별로 재료 리스트 조회: 
        # [Ingredients(ingredients: [Ingredient, Ingredient]), Ingredients(ingredients: [Ingredient, Ingredient])]
        ingredients_list = [
            self.recipes_repository.select_ingredients_by_ingredients_id(recipe.get_ingredients()) 
            for recipe in recipes.get_recipes()
            ]
        return ingredients_list


    def update_cooked_recipes(self, user_id: str, recipes_id: str, feedback: bool):
        user = self.get_user_by_user_id(user_id)
        user_cooked_recipes_id = self.get_user_cooked_recipes_id_by_user(user)
        user_recommended_recipes_id = self.get_user_recommended_recipes_id_by_user(user)
        if feedback:
            user_recommended_recipes_id.remove(recipes_id)
            user_cooked_recipes_id.append(recipes_id)
            return self.recipes_repository.update_cooked_recipes(user_id, user_cooked_recipes_id, user_recommended_recipes_id)
        user_cooked_recipes_id.remove(recipes_id)
        user_recommended_recipes_id.append(recipes_id)
        return self.recipes_repository.update_cooked_recipes(user_id, user_cooked_recipes_id, user_recommended_recipes_id)
    
    def get_prices_by_ingredients_id(self, ingredients_id: List[str]):
        ingredients = self.recipes_repository.select_ingredients_by_ingredients_id(ingredients_id).get_ingredients()
        return {ingredient.get_id(): ingredient.get_price() for ingredient in ingredients}
    
    def get_ingredients_by_ingredients_id(self, ingredients_id: List[str]):
        return self.recipes_repository.select_ingredients_by_ingredients_id(ingredients_id).get_ingredients()
