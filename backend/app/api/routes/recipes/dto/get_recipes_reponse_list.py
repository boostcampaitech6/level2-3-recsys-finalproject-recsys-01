from ..entity.recipes import Recipes
from ..entity.ingredients import Ingredients
from .get_recipes_reponse import GetRecipesReponse
from typing import List


class GetRecipesReponseList:
  recipe_list: List[GetRecipesReponse]
  cooked_recipes_id: List[str] 
  next_page_url: str 
  
  def __init__(self, recipes: Recipes, ingredients_list: List[Ingredients], cooked_recipes_id: List[str] = None, next_page_url: str = None):
    super().__init__() 
    self.recipe_list = list()
    for recipe, ingredients in zip(recipes.get_recipes(), ingredients_list):
      id = recipe.get_id()
      recipe_name = recipe.get_recipe_name()
      recipe_url = recipe.get_recipe_url()
      response_ingredients = self._make_ingredient_dict(ingredients)
      recipe_img_url = recipe.get_recipe_img_url()
      self.recipe_list.append(GetRecipesReponse(
        id = id, recipe_name=recipe_name, recipe_url=recipe_url, 
        ingredient=response_ingredients, recipe_img_url=recipe_img_url))
    self.cooked_recipes_id = cooked_recipes_id
    self.next_page_url = next_page_url
 
 
  def _make_ingredient_dict(self, ingredients: Ingredients):
    result = {ingredient.get_id(): ingredient.get_name() for ingredient in ingredients.get_ingredients()}
    return result
  
        