from pydantic import BaseModel
from typing import List
from .ingredient import Ingredient


class Ingredients(BaseModel):
    ingredients: List[Ingredient]
    
    def get_ingredients(self):
        return self.ingredients