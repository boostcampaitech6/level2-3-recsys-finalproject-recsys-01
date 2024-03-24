from fastapi import HTTPException
from bson import ObjectId
from typing import List
from app.database.data_source import data_source
from ..entity.user import User
from ..entity.recipes import Recipes
from ..entity.ingredients import Ingredients

import logging

logging.basicConfig(level=logging.DEBUG)


class RecipesRepository:
    def __init__(self):
        self.users_collection = data_source.collection_with_name_as("users")
        self.recipes_collection = data_source.collection_with_name_as("recipes")
        self.ingredients_collection = data_source.collection_with_name_as("ingredients")
        self.amounts_collection = data_source.collection_with_name_as("amounts")
        self.prices_collection = data_source.collection_with_name_as("prices")

    def select_user_by_user_id(self, login_id: str) -> User:
        user = self.users_collection.find_one({"login_id": login_id})
        if user:
            return User(**user)
        raise HTTPException(status_code=404, detail=f"User {id} not found")


    def select_recipes_by_recipes_id(self, recipes_id: List[str]) -> Recipes:
        recipes = Recipes(recipes = self.recipes_collection.find({"_id": { "$in": list(map(ObjectId, recipes_id))} }))
        if recipes:
            return recipes
        raise HTTPException(status_code=404, detail=f"Recipes not found")


    def select_ingredients_by_ingredients_id(self, ingredients_id: List[str]) -> Ingredients:
        # logging.debug("----------[Recipe Repository]-----------")
        # ingredients = list(self.ingredients_collection.find({"_id": { "$in": list(map(ObjectId, ingredients_id))} }))
        amounts = list(self.amounts_collection
                       .find({"_id": { "$in": list(map(ObjectId, ingredients_id))} })
                       .sort({'ingredient_id': 1}))
        ingredient_ids = [amount['ingredient_id'] for amount in amounts]
        ingredients = list(self.ingredients_collection
                           .find({"_id": {"$in": list(map(ObjectId, ingredient_ids))}})
                           .sort({'_id': 1}))
        prices = list(next(self.prices_collection
                  .find({"ingredient_id": ingredient_id}).sort({"date": -1}).limit(1)) for ingredient_id in ingredient_ids)
        # prices = list(self.prices_collection.find({"ingredient_id": {"$in": list(map(ObjectId, ingredient_ids))}}))

        # logging.debug(len(amounts), len(ingredients), len(prices))
        ingredient_list = list()
        for amount, ingredient, price in zip(amounts, ingredients, prices):
            # id: PyObjectId = Field(alias='_id', default=None)
            # name: str
            # price: float
            # price_url: str
            # amount: dict
            amount['name'] = ingredient['name']
            amount['price'] = price['price']
            amount['price_url'] = price['price_url']
            amount['amount'] = {
                'value': amount['value'],
                'unit': amount['unit'],
            }
            ingredient_list.append(amount)
        
        # logging.debug('[RECIPE_REPOSITORY_RESULT]', ingredient_list)
        ingredients = Ingredients(ingredients = ingredient_list)
        # logging.debug('ingredients', ingredients.get_ingredients())
        if ingredients:
            return ingredients
        raise HTTPException(status_code=404, detail=f"Ingredients not found")


    def update_cooked_recipes(self, login_id: str, user_cooked_recipes_id: List[str], user_recommended_recipes_id: List[str]) -> bool:
        update_result = self.users_collection.update_one(
            {"login_id": login_id},
            {"$set": {
                "feedback_history": user_cooked_recipes_id,
                "recommend_history_by_basket": user_recommended_recipes_id
            }}
        )
        return update_result.modified_count > 0
        
