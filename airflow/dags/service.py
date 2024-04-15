from __future__ import annotations
import bentoml
import threading  # threading 라이브러리 추가

from db_operations import fetch_user_history, update_model_recommendations, cb_inference, blending_results
from _recbole_inference import Inference

@bentoml.service(
    resources={"cpu": "6"},
    traffic={"timeout": 20},
)
class OnlineServing:
    def __init__(self) -> None:

        # 설정 파일과 모델 저장 경로 설정
        modelpath = '/home/judy/level2-3-recsys-finalproject-recsys-01/ml/Sequential/saved/SASRec-Mar-29-2024_19-28-51.pth'
        self.inferencer = Inference(modelpath)

    def save_data_async(self, data, collection_name, input_type='recipe_sno', meta={}):
        # 데이터 저장 작업을 비동기적으로 수행
        update_model_recommendations(
            data, 
            collection_name=collection_name,
            input_type=input_type,
            meta=meta,
        )

    @bentoml.api
    def recommend(self, user_id: str):

        hybrid_data = fetch_user_history(user_id)
        hybrid_data = self.inferencer.sasrec_inference(hybrid_data)

        cb_data = fetch_user_history(user_id, result_type='recipe_id')
        cb_data = cb_inference(cb_data)

        data = blending_results(hybrid_data, cb_data)
        
        update_model_recommendations(
            data, 
            collection_name='model_recommendation_history_total', 
            input_type='recipe_id',
            meta={'model_version': '0.0.1'},
        )

        # 비동기로 DB에 결과 기록
        threading.Thread(target=self.save_data_async, args=(hybrid_data, 'model_recommendation_history_hybrid',)).start()
        threading.Thread(target=self.save_data_async, args=(cb_data, 'model_recommendation_history_cb', 'recipe_id',)).start()


        return { "message": "Prediction successful" }
