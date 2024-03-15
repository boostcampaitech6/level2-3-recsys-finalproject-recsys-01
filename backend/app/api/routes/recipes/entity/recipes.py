from pydantic import BaseModel
from typing import List
from .recipe import Recipe


class Recipes(BaseModel):
    recipes: List[Recipe]
    
    def get_recipes(self):
        return self.recipes
        