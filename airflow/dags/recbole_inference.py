import math
from typing import List

import torch

from recbole.quick_start import load_data_and_model
from recbole.data.interaction import Interaction

def prep_inference_data(user_id_and_feedbacks, dataset, config) -> Interaction:

    item_id_list, item_length = [], []
    for user_id_and_feedback in user_id_and_feedbacks:

        # 레시피토큰 -> id 로 변환
        recipe_ids = [dataset.token2id(dataset.iid_field, item_token) for item_token in user_id_and_feedback['feedbacks']]

        item_id_list.append(recipe_ids) 
        item_length.append(len(recipe_ids))

    max_length = 100 # max(len(sublist) for sublist in item_id_list)
    padded_item_id_list = [sublist + [0]*(max_length - len(sublist)) for sublist in item_id_list]

    item_dict = {
        'item_id_list': torch.tensor(padded_item_id_list, dtype=torch.int64).to(config['device']),
        'item_length': torch.tensor(item_length, dtype=torch.int64).to(config['device'])
    }

    # Interaction 객체 생성
    interaction = Interaction(item_dict)

    return interaction, item_id_list 

def sasrec_inference(modelpath: str, user_id_and_feedbacks: list, k: int=20, batch_size: int=4096):

    num_users = len(user_id_and_feedbacks)
    recommended_result = []

    # 저장된 아티팩트 로드
    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(modelpath)

    for i in range(math.ceil(num_users/batch_size)):

        # prep data
        batch_data = user_id_and_feedbacks[i*batch_size: (i+1)*batch_size]
        user_ids = [data['_id'] for data in batch_data]
        inference_data, item_id_list = prep_inference_data(batch_data, dataset, config)

        # prediction
        scores = model.full_sort_predict(inference_data).view(num_users, -1)
        probas = torch.sigmoid(scores).detach().cpu()

        # masking - 언젠가 해야 함
        for proba, item_ids in zip(probas, item_id_list):
            proba[item_ids] = 0

        # 확률이 높은 아이템 20개 추출 
        topk_proba, topk_item = torch.topk(probas, k, dim=1)

        # recipe id to token
        recipe_tokens = [
            dataset.id2token(dataset.iid_field, item_token).tolist()\
                for item_token in topk_item.detach().cpu().numpy()]

        for user, recommended_items in zip(user_ids, recipe_tokens):
            recommended_result.append({
                '_id': user,
                'recommended_items': recommended_items
            })

    return recommended_result

if __name__ == '__main__':

    # 설정 파일과 모델 저장 경로 설정
    modelpath = '/home/judy/level2-3-recsys-finalproject-recsys-01/ml/Sequential/saved/SASRec-Mar-25-2024_03-39-27.pth'

    from db_operations import fetch_user_histories 

    # 데이터 얻기
    user_id_and_feedbacks = fetch_user_histories()

    recommended_items = sasrec_inference(
        modelpath, 
        user_id_and_feedbacks)

    from bson import ObjectId
    from pymongo import MongoClient
    from db_config import db_host, db_port

    # 추천 결과 확인하기
    client = MongoClient(host=db_host, port=db_port)
    db = client.dev

    for feedback, recommended_item in zip(user_id_and_feedbacks, recommended_items):
        print(recommended_item['_id'])
        for recipe in feedback['feedbacks']:
            for r in db['recipes'].find({'recipe_sno': recipe}):
                print(r['food_name'], end=' | ')
        print()
        for recipe in recommended_item['recommended_items']:
            for r in db['recipes'].find({'recipe_sno': recipe}):
                print(r['food_name'], end=' | ')
        print()
