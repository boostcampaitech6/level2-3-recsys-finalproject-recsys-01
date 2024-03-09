import os

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

def env_file_of(env: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{env}.env")

class DataSource(BaseModel):
    host: str
    port: str
    database_name: str
    client: Optional[object] = None

    def collection_with_name_as(self, name: str) -> Collection:
        if self.client is None:
            self._make_connection()
        return self.client[self.database_name][name]
    
    def database(self) -> Database:
        if self.client is None:
            self._make_connection()
        return self.client[self.database_name]

    def _make_connection(self) -> None:
        self.client = MongoClient(f"mongodb://{self.host}:{self.port}/")

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
