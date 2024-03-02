import pandas as pd
from pymongo import MongoClient

# MongoDB 연결 설정
client = MongoClient('mongodb://localhost:27017/')
db = client['database']  # 데이터베이스 선택
collection = db['test']  # 컬렉션 선택

# CSV 파일 읽기
PATH = 'reviews_240302.csv'
data = pd.read_csv(PATH)

# MongoDB에 데이터 삽입
records = data.to_dict(orient='records')
collection.insert_many(records)