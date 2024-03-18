from pydantic import BaseModel, Field, ConfigDict
from utils.pyobject_id import PyObjectId


class Ingredient(BaseModel):
    id: PyObjectId = Field(alias='_id', default=None)
    name: str
    price: float
    price_url: str
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "recipe_id",
                "name": "김치",
                "price": "5800",
                "price_url": "https://www.10000recipe.com/recipe/view.html?seq=6908832&targetList=reviewLists#reviewLists",
            }
        },
    )
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_price(self):
        return self.price
