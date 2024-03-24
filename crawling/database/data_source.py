import os

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

from exception.database import (
    DatabaseNotFoundException, CollectionNotFoundException
)

def env_file_of(env: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{env}.env")

class DataSource(BaseModel):
    host: str
    port: str
    database_name: str
    client: Optional[object] = None

    def database(self) -> Database:
        if self.client is None:
            self._make_connection()
        
        self._validate_database()
        return self.client[self.database_name]
    
    def collection_with_name_as(self, collection_name: str) -> Collection:
        if self.client is None:
            self._make_connection()
        
        self._validate_collection(collection_name)
        return self.client[self.database_name][collection_name]

    def _make_connection(self) -> None:
        url = f"mongodb://{self.host}:{self.port}/"
        self.client = MongoClient(url)
    
    def _validate_database(self) -> None:
        database_names = self.client.list_database_names()
        if self.database_name not in database_names:
            raise DatabaseNotFoundException(f"해당하는 데이터베이스가 존재하지 않습니다: {self.database_name}")

    def _validate_collection(self, collection_name) -> None:
        collection_names = self.client[self.database_name].list_collection_names()
        if collection_name not in collection_names:
            raise CollectionNotFoundException(f"해당하는 컬렉션이 존재하지 않습니다: {collection_name}")


env_name = os.getenv('ENV', 'dev')
file_path = env_file_of(env_name)
assert os.path.exists(file_path), f"파일이 존재하지 않습니다: {file_path}"

load_dotenv(file_path)

data_env = {
    'host': os.getenv('HOST'),
    'port': os.getenv('PORT'),
    'database_name': os.getenv('DATABASE'),
}

data_source = DataSource(**data_env)
