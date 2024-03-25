from datetime import datetime as dt
from tqdm import tqdm
from pymongo import MongoClient

def main():
    client = MongoClient(host='10.0.7.6', port=27017)
    db = client.dev

    data = []
    exist_recipes = [recipe['_id'] for recipe in db['train_recipes'].find()]

    # recipes 조회
    num_recipes = db['recipes'].count_documents({})
    for i, r in tqdm(enumerate(db['recipes'].find()), total=num_recipes):
        if r['_id'] in exist_recipes: continue
        data.append({   
            '_id': r['_id'],
            'food_name': r['food_name'],
        })
        print(str(r['_id']), r['food_name'])

    # 업데이트 데이터 개수 확인
    print(len(data))

    # 업데이트
    print('before update: ', db['train_recipes'].count_documents({}))
    db['train_recipes'].insert_many(data)

    # 결과
    print('after update:  ', db['train_recipes'].count_documents({}))

if __name__ == '__main__':
    main()
