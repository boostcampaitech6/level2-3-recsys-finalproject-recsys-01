import math
from datetime import datetime as dt

import numpy as np
from tqdm import tqdm

from pymongo import MongoClient

import faiss

def main():
    client = MongoClient(host='10.0.7.6', port=27017)
    db = client.dev
    collection = db['recipes']

    # 업데이트
    print('before update: ', collection.count_documents({}))
    
    ids = list()
    names = list()
    embeddings = list()
    for recipe in collection.find():
        if 'food_embedding' in recipe:
            ids.append(recipe['_id'])
            embeddings.append(recipe['food_embedding'])
            names.append(recipe['food_name'])
    embeddings = np.array(embeddings).astype('float32')

    d = 768
    index = faiss.IndexFlatL2(d)   # build the index
    index.add(embeddings)
    print(f'{dt.now()} index added')

    # find
    k = 10                          # we want to see 4 nearest neighbors
    D, I = index.search(embeddings, k) # sanity check
    print(f'{dt.now()} searched')

    # update collection
    for recipe_id, similar_idx in zip(ids, I):
        closest_idx = similar_idx[1]
        for idx in similar_idx[1:]:
            if names[similar_idx[0]] == names[idx]:
                continue
            else:
                closest_idx = idx
                break

        collection.update_one(
            {'_id': recipe_id}, 
            {'$set': {'closest_recipe': ids[closest_idx]}})
    
#    for i, recipe in zip(range(10), collection.find()):
#        print(recipe['food_name'], '|\t', collection.find({'_id':recipe['closest_recipe']})[0]['food_name'])

if __name__ == '__main__':
    main()
