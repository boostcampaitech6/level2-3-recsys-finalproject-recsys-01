import math
from datetime import datetime as dt
from tqdm import tqdm
from pymongo import MongoClient

from transformers import BertTokenizer, BertModel
import torch

def embedding_k_food_names(food_names):
    # 한국어 BERT 사전 훈련된 모델 로드
    tokenizer = BertTokenizer.from_pretrained('klue/bert-base')
    model = BertModel.from_pretrained('klue/bert-base')

    # 텍스트를 토큰화하고 BERT 입력 형식에 맞게 변환
    inputs = tokenizer(food_names, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # BERT 모델을 통해 텍스트 인코딩
    with torch.no_grad():
        outputs = model(**inputs)

    # 마지막 은닉층의 특징 벡터를 추출
    last_hidden_states = outputs.last_hidden_state

    # 첫 번째 토큰([CLS] 토큰)의 은닉 상태를 문장의 임베딩으로 사용
    sentence_embedding = last_hidden_states[:, 0, :]

    return sentence_embedding.tolist()

def main():
    client = MongoClient(host='10.0.7.6', port=27017)
    db = client.dev
    collection = db['train_recipes']

    # 업데이트
    print('before update: ', collection.count_documents({}))

    batch_size = 512
    offset = 0

    for offset in tqdm(range(math.ceil(collection.count_documents({})/512))):
        offset *= batch_size 

        # 컬렉션에서 100개씩 문서를 조회
        food_names = [recipe['food_name'] for recipe in collection.find().skip(offset).limit(batch_size)]
        # food_embedding
        food_embeddings = embedding_k_food_names(food_names)

        # update collection
        for recipe, food_embedding in zip(collection.find().skip(offset).limit(batch_size), food_embeddings):
            collection.update_one(
                {'_id': recipe['_id']}, 
                {'$set': {'food_embedding': food_embedding}})
    
    for i, recipe in zip(range(10), collection.find()):
        print(i, len(recipe['food_embedding']))


if __name__ == '__main__':
    main()
