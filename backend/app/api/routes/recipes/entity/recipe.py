from pydantic import BaseModel, Field, ConfigDict
from .....utils.pyobject_id import PyObjectId
from typing import List


class Recipe(BaseModel):
    id: PyObjectId = Field(alias='_id', default=None)
    food_name: str
    recipe_name: str
    ingredient: List[PyObjectId] = []
    time_taken: int
    difficulty: str
    recipe_url: str
    portion: str
    recipe_img_url: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "recipe_id",
                "food_name": "김치찌개",
                "recipe_name": "매콤한 김치찌개",
                "ingredient": [],
                "time_taken": 30,
                "difficulty": "중급",
                "recipe_url": "https://www.10000recipe.com/recipe/view.html?seq=6908832&targetList=reviewLists#reviewLists",
                "portion": "4인분",
                "recipe_img_url": "https://recipe1.ezmember.co.kr/cache/recipe/2019/03/10/ad0e61fd8b4783a926ebccadd0c1b8c11.jpg"
            }
        },
    )
    
    
    def get_id(self):
        return self.id
    
    
    def get_recipe_name(self):
        return self.recipe_name
    
    
    def get_recipe_url(self):
        return self.recipe_url
    
    
    def get_recipe_img_url(self):
        return self.recipe_img_url
    
    
    def get_ingredients(self):
        return self.ingredient
