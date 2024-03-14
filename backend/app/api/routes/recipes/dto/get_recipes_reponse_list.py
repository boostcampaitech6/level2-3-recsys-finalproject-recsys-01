from ..entity.recipes import Recipes
from ..entity.ingredients import Ingredients
from .get_recipes_reponse import GetRecipesReponse
from typing import List


class GetRecipesReponseList:
  response: List[GetRecipesReponse]
 
  def __init__(self, recipes: Recipes, ingredients_list: List[Ingredients]):
    super().__init__() 
    self.response = list()
    for recipe, ingredients in zip(recipes.get_recipes(), ingredients_list):
      id = recipe.get_id()
      recipe_name = recipe.get_recipe_name()
      recipe_url = recipe.get_recipe_url()
      response_ingredients = self._make_ingredient_dict(ingredients)
      recipe_img_url = recipe.get_recipe_img_url()
      self.response.append(GetRecipesReponse(
        id = id, recipe_name=recipe_name, recipe_url=recipe_url, 
        ingredient=response_ingredients, recipe_img_url=recipe_img_url))
  
 
  def _make_ingredient_dict(self, ingredients: Ingredients):
    result = {ingredient.get_id(): ingredient.get_name() for ingredient in ingredients.get_ingredients()}
    return result
  
        