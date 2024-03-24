from pydantic import BaseModel, Field, ConfigDict
from app.utils.pyobject_id import PyObjectId


class Ingredient(BaseModel):
    id: PyObjectId = Field(alias='_id', default=None)
    name: str
    price: float
    price_url: str
    amount: dict
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "recipe_id",
                "name": "김치",
                "price": "5800",
                "amount": { "value": 240, "unit": 'g' },
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
    
    def as_basket_form(self):
        '''{
			"ingredient_id": 10,
			"ingredient_name": "브로콜리",
			"ingredient_amount": 1,
			"ingredient_unit": "kg",
			"ingredient_price": "4680",
			"img_link": "https://health.chosun.com/site/data/img_dir/2024/01/19/2024011902009_0.jpg",
			"market_url":
			"https://www.coupang.com/vp/products/4874444452?itemId=6339533080&vendorItemId=73634892616&pickType=COU_PICK&q=%EB%B8%8C%EB%A1%9C%EC%BD%9C%EB%A6%AC&itemsCount=36&searchId=891d0b69dc8f452daf392e3db2482732&rank=1&isAddedCart="
		}'''

        return {
            'ingredient_id': self.id,
            'ingredient_name': self.name,
            'ingredient_amount': self.amount['value'],
            'ingredient_unit': self.amount['unit'],
            'ingredient_price': self.price,
            'img_link': 'https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg',
            'market_url': self.price_url,
        }
