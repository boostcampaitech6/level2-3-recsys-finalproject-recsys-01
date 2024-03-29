from datetime import datetime as dt

from bson import ObjectId
from pymongo import MongoClient

from db_config import db_host, db_port

def fetch_user_history(user_id, result_type='recipe_sno'):

    # db setting
    client = MongoClient(host=db_host, port=db_port)
    db = client.dev

    # user
    user_id_and_feedbacks = []
    for u in db['users'].find({'_id': ObjectId(user_id)}):
        # initial_feedback이 있음
        feedbacks = u['initial_feedback_history']
        # 추가 피드백 있는 경우
        if 'feedback_history' in u:
            feedbacks.append(u['feedback_history'])
        # 피드백 _id를 recipe_sno 로 변경
        recipe_snos = []
        for recipe in feedbacks:
            for r in db['recipes'].find({'_id': ObjectId(recipe)}):
                recipe_snos.append(r['recipe_sno'])

        if result_type == 'recipe_sno':
            user_id_and_feedbacks.append({
                '_id': str(u['_id']),
                'feedbacks': recipe_snos,
                })
        else:
            user_id_and_feedbacks.append({
                '_id': str(u['_id']),
                'feedbacks': [str(feedback) for feedback in feedbacks],
                })

    return user_id_and_feedbacks

def fetch_user_histories(result_type='recipe_sno'):

    # db setting
    client = MongoClient(host=db_host, port=db_port)
    db = client.dev

    # user
    user_id_and_feedbacks = []
    for u in db['users'].find({}):
        # initial_feedback이 있음
        feedbacks = u['initial_feedback_history']
        # 추가 피드백 있는 경우
        if 'feedback_history' in u:
            feedbacks.extend(u['feedback_history'])

        # 피드백 _id를 recipe_sno 로 변경
        recipe_snos = []
        for recipe in feedbacks:
            for r in db['recipes'].find({'_id': ObjectId(recipe)}):
                recipe_snos.append(r['recipe_sno'])

        if result_type == 'recipe_sno':
            user_id_and_feedbacks.append({
                '_id': str(u['_id']),
                'feedbacks': recipe_snos,
                })
        else:
            user_id_and_feedbacks.append({
                '_id': str(u['_id']),
                'feedbacks': [str(feedback) for feedback in feedbacks],
                })


    return user_id_and_feedbacks


def update_model_recommendations(recommended_results, collection_name, meta={}, input_type='recipe_sno'):

    # db setting
    client = MongoClient(host=db_host, port=db_port)
    db = client.dev

    if input_type == 'recipe_sno':
        for recommended_result in recommended_results:
            recommended_items = []
            for recipe in recommended_result['recommended_items']:
                for r in db['recipes'].find({'recipe_sno': recipe}):
                    recommended_items.append(r['_id'])
                    break
            recommended_result['recommended_items'] = recommended_items

        data = [{
            'user_id': ObjectId(recommended_result['_id']), 
            'recommended_recipes': recommended_result['recommended_items'], 
            'datetime': dt.now(),
            **meta
            } for recommended_result in recommended_results]
    else:
        data = [{
            'user_id': ObjectId(recommended_result['_id']), 
            'recommended_recipes': [ObjectId(recipe_id) for recipe_id in recommended_result['recommended_items']], 
            'datetime': dt.now(),
            **meta
            } for recommended_result in recommended_results]

    db[collection_name].insert_many(data)

    print('push data into db')

def cb_inference(user_id_and_feedbacks: list, k: int=20, batch_size: int=4096):

    # db setting
    client = MongoClient(host=db_host, port=db_port)
    db = client.dev

    recommended_results = []
    for user_data in user_id_and_feedbacks:
        user_recommended = []
        for feedback in user_data['feedbacks'][::-1][:10]:
            for r in db['train_recipes'].find({'_id': ObjectId(feedback)}):
                user_recommended.append(str(r['closest_recipe']))
                break

        recommended_results.append({
            '_id': user_data['_id'],
            'recommended_items': user_recommended
        })
        
    return recommended_results 

def blending_results(hybrid_results, cb_results):

    # db setting
    client = MongoClient(host=db_host, port=db_port)
    db = client.dev

    # hybrid tokens to recipe id
    for recommended_result in hybrid_results:
        recommended_items = []
        for recipe in recommended_result['recommended_items']:
            for r in db['recipes'].find({'recipe_sno': recipe}):
                recommended_items.append(str(r['_id']))
                break
        recommended_result['recommended_items'] = recommended_items

    blended_results = []
    for user_hybrid, user_cb in zip(hybrid_results, cb_results):

        user_id = user_hybrid['_id']
        blended_result = set(user_hybrid['recommended_items'][:10] + user_cb['recommended_items'])

        i = 10
        while len(blended_result) < 20:
            blended_result = blended_result | {user_hybrid['recommended_items'][i]}
            i += 1

        blended_results.append({
            '_id': user_id,
            'recommended_items': list(blended_result)
        })

    return blended_results

if __name__ == '__main__':

    # 데이터 얻기
    user_id_and_feedbacks = fetch_user_history(result_type='recipe_id')

    recommended_items = cb_inference(
        user_id_and_feedbacks)

    print(recommended_items)

    # 추천 결과 확인하기
    client = MongoClient(host=db_host, port=db_port)
    db = client.dev

    for recommended_item in recommended_items:
        print(recommended_item['_id'])
        for recipe in recommended_item['recommended_items']:
            for r in db['recipes'].find({'_id': recipe}):
                print(r['food_name'], end=' | ')
        print()
