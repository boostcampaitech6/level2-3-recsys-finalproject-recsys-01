from pydantic import BaseModel
from utils.pyobject_id import PyObjectId
from typing import Dict


class GetRecipesReponse(BaseModel):
    id: PyObjectId
    recipe_name: str
    ingredient: Dict[PyObjectId, str] = {}
    recipe_url: str
    recipe_img_url: str
    
    