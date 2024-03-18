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
        logging.debug(result)
        return result
    
    def update_food(self, login_id: str, foods: list) -> int:
        query = {'login_id': login_id}
        update_value = {'$set': {'initial_feedback_history': foods}}
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
        self.collection = data_source.collection_with_name_as('foods')

    def find_foods(self, page_num: int, page_size: int=10) -> list:
        skip_count: int = (page_num - 1) * page_size
        results = self.collection.find().sort([('name', pymongo.ASCENDING)]).skip(skip_count).limit(page_size)
        lst = []
        for result in results:
            result['_id'] = str(result['_id'])
            lst.append(result)
        return lst
    
class RecommendationRepository:
    def __init__(self):
        self.collection = data_source.collection_with_name_as('model_recommendation_histories')

    def find_by_login_id(self, login_id: str) -> list:
        result = self.collection.find_one({'id': login_id})
        return result['recommended_item']
    
    def save(self, recommendation):
        self.collection.insert_one(recommendation)
