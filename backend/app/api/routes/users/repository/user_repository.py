from .....database.data_source import data_source
from ..dto.user_dto import UserSignupDTO

class UserRepository:
    def __init__(self):
        self.collection = data_source.collection_with_name_as('users')

    def insert_one(self, user: UserSignupDTO) -> UserSignupDTO:
        self.collection.insert_one(user)
        return UserSignupDTO(**self.collection.find_one(user))

    def all_users(self) -> list[UserSignupDTO]:
        return [UserSignupDTO(**user) for user in self.collection.find()]
    
    def find_one(self, id: str) -> UserSignupDTO:
        return UserSignupDTO(**self.collection.find_one({'_id': id}))