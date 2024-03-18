from pydantic import BaseModel
from typing import List
from .recipe import Recipe


class Recipes(BaseModel):
    recipes: List[Recipe]
    
    def get_recipes(self):
        return self.recipes
        
    def get_ingredients(self):
        return set.union(*(set(recipe.get_ingredients()) for recipe in self.recipes))