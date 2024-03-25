from datetime import datetime
from app.database.data_source import data_source
from ..dto.user_dto import UserSignupDTO, UserLoginDTO
import logging
import pymongo

logging.basicConfig(level=logging.DEBUG)

class UserRepository:
    def __init__(self):
        self.collection = data_source.collection_with_name_as('users')

    def insert_one(self, user: UserSignupDTO) -> UserSignupDTO:
        result = self.collection.insert_one(dict(user))
        return UserSignupDTO(
            _id=result.inserted_id,
            login_id=user.login_id,
            password=user.password,
            nickname=user.nickname,
            email=user.email)

    def all_users(self) -> list[UserSignupDTO]:
        return [UserSignupDTO(**user) for user in self.collection.find()]
    
    def find_one(self, query: dict) -> UserSignupDTO:
        result = self.collection.find_one(query)
        # logging.debug(result)
        return result
    
    def update_food(self, login_id: str, foods: list) -> str:
        query = {'login_id': login_id}
        update_value = {'$set': {'initial_feedback_history': foods}}
        self.collection.update_one(query, update_value)

        user = self.collection.find_one(query)
        return str(user['_id'])
    
    def update_recommended_basket(self, login_id: str, recipe_list: list):
        query = {'login_id': login_id}
        update_value = {'$addToSet': {'recommend_history_by_basket': {'$each': recipe_list}}}
        result = self.collection.update_one(query, update_value)
        return result.modified_count
    
class SessionRepository:
    def __init__(self):
        self.collection = data_source.collection_with_name_as('sessions')

    def insert_one(self, login_id: str, token: str, expire_date: datetime) -> UserLoginDTO:
        result = self.collection.insert_one({'login_id': login_id, 'token': token, 'expire_date': expire_date})
        if result.inserted_id is None:
            raise ValueError("세션 생성이 실패했습니다.")
        return UserLoginDTO(token=token, login_id=login_id, password='')
    
    def find_one(self, id: str) -> UserLoginDTO:
        return UserLoginDTO(**self.collection.find_one({'_id': id}))
    
class FoodRepository:
    def __init__(self):
        self.collection = data_source.collection_with_name_as('recipes')

    def find_foods(self, page_num: int, page_size: int=16) -> list:
        skip_count: int = (page_num - 1) * page_size
        results = self.collection.find().sort([('_id', pymongo.ASCENDING)]).skip(skip_count).limit(page_size + 1)
        # logging.debug(results)
        results = list(results)
        total_size = len(results)
        # logging.debug('total_size', total_size)
        lst = []
        for i, result in enumerate(results):
            if i == page_size: break
            result['_id'] = str(result['_id'])
            del result['ingredients']
            lst.append(result)

        return lst, (total_size > page_size)
    
class RecommendationRepository:
    def __init__(self):
        self.collection = data_source.collection_with_name_as('model_recommendation_histories')

    def find_by_user_id(self, user_id: str) -> list:
        result = self.collection.find({'id': user_id}).sort({'datetime':-1}).limit(1)
        result = next(result, None)
        return result['recommended_item'] if (result and 'recommended_item' in result) else []

class BasketRepository:
    def __init__(self):
        self.collection = data_source.collection_with_name_as('baskets')

    def save(self, recommendation):
        self.collection.insert_one(recommendation)
