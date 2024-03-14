from fastapi import HTTPException
from bson import ObjectId
from typing import List
from .....database.data_source import data_source
from ..entity.user import User
from ..entity.recipes import Recipes
from ..entity.ingredients import Ingredients

users_collection = data_source.collection_with_name_as("users")


def select_user_by_user_id(user_id: str) -> User:
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(**user)
    raise HTTPException(status_code=404, detail=f"User {id} not found")


def select_recipes_by_recipes_id(recipes_id: List[str]) -> Recipes:
    recipes_collection = data_source.collection_with_name_as("recipes")
    recipes = Recipes(recipes = recipes_collection.find({"_id": { "$in": list(map(ObjectId, recipes_id))} }))
    if recipes:
        return recipes
    raise HTTPException(status_code=404, detail=f"Recipes not found")


def select_ingredients_by_ingredients_id(ingredients_id: List[str]) -> Ingredients:
    ingredients_collection = data_source.collection_with_name_as("ingredients")
    ingredients = Ingredients(ingredients = ingredients_collection.find({"_id": { "$in": list(map(ObjectId, ingredients_id))} }))
    if ingredients:
        return ingredients
    raise HTTPException(status_code=404, detail=f"Ingredients not found")


def update_cooked_recipes(user_id: str, user_cooked_recipes_id: List[str], user_recommended_recipes_id: List[str]) -> bool:
    update_result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "feedback_history": user_cooked_recipes_id,
            "recommend_history_by_basket": user_recommended_recipes_id
        }}
    )
    return update_result.modified_count > 0
    
