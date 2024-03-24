from datetime import datetime as dt

from bson import ObjectId
from pymongo import MongoClient

from db_config import db_host, db_port

def fetch_user_history():

    # db setting
    client = MongoClient(host=db_host, port=db_port)
    db = client.dev

    # user
    user_id_and_feedbacks = []
    for u in db['users'].find({'_id':ObjectId('65fe8ede5b23f8126f66ffa2')}): # 원랜 여기가 find()
        # initial_feedback이 있음
        feedbacks = u['initial_feedback_history']
        # 추가 피드백 있는 경우
        if 'feedback_history' in u:
            feedbacks.append(u['feedback_history'])
        # 피드백 _id를 recipe_sno 로 변경
        recipe_snos = []
        for recipe in feedbacks:
            for r in db['recipes'].find({'_id': recipe}):
                recipe_snos.append(r['recipe_sno'])

        user_id_and_feedbacks.append({
            '_id': str(u['_id']),
            'feedbacks': recipe_snos,
            })

    return user_id_and_feedbacks


def update_model_recommendations(recommended_results, collection_name, meta={}):

    # db setting
    client = MongoClient(host=db_host, port=db_port)
    db = client.dev

    #print(recommended_results)
    for recommended_result in recommended_results:
        # print(recommended_result['_id'])
        recommended_items = []
        for recipe in recommended_result['recommended_items']:
            for r in db['recipes'].find({'recipe_sno': recipe}):
                recommended_items.append(r['_id'])
                # print(r['food_name'], end=' | ')
                break
        recommended_result['recommended_items'] = recommended_items

    data = [{
        'user_id': ObjectId(recommended_result['_id']), 
        'recommended_recipes': recommended_result['recommended_items'], 
        'datetime': dt.now(),
        **meta
        } for recommended_result in recommended_results]

    db[collection_name].insert_many(data)

    print('push data into db')
