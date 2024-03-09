import os

from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv
from pydantic import BaseModel

def env_file_of(env: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{env}.env")

class DataSource(BaseModel):
    host: str
    port: str
    database: str

    def make_connection(self) -> None:
        self.client = MongoClient(f"mongodb://{self.host}:{self.port}/")
    
    def collection_with_name_as(self, name: str) -> Collection:
        return self.client[self.database][name]

env_name = os.getenv('ENV', 'dev')
file_path = env_file_of(env_name)
assert os.path.exists(file_path), f"파일이 존재하지 않습니다: {file_path}"

load_dotenv(file_path)

data_env = {
    'host': os.getenv('HOST'),
    'port': os.getenv('PORT'),
    'database': os.getenv('DATABASE'),
}

data_source = DataSource(**data_env)
