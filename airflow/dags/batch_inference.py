from pymongo import MongoClient

from datetime import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from db_config import db_host, db_port

from db_operations import fetch_user_history, update_model_recommendations
from recbole_inference import sasrec_inference 

def fetch_and_push_user_history(**context):
    user_id_and_feedbacks = fetch_user_history()
    context["ti"].xcom_push(key='user_id_and_feedbacks', value=user_id_and_feedbacks)

def batch_inference(**context):
    user_id_and_feedbacks = context["ti"].xcom_pull(key='user_id_and_feedbacks')

    # 설정 파일과 모델 저장 경로 설정
    modelpath = '/home/judy/level2-3-recsys-finalproject-recsys-01/ml/Sequential/saved/BERT4Rec-Mar-24-2024_00-51-09.pth'

    recommended_results = sasrec_inference(
        modelpath, 
        user_id_and_feedbacks)

    context["ti"].xcom_push(key='recommended_results', value=recommended_results)

def save_results(collection_name, **context):
    recommended_results = context["ti"].xcom_pull(key='recommended_results')
    update_model_recommendations(recommended_results, collection_name)

with DAG(
        dag_id="batch_inference",
        description="batch inference of all active users using MultiDAE",
        start_date=days_ago(5), # DAG 정의 기준 2일 전부터 시작합니다. 
        schedule_interval="0 2 * * *", # 매일 2시에 시작
        tags=["basket_recommendation", "inference"],
        ) as dag:

    # get active user 
    t1 = PythonOperator(
        task_id="fetch_and_push_user_history",
        python_callable=fetch_and_push_user_history,
        depends_on_past=False, 
        owner="judy",
        retries=3,
        retry_delay=timedelta(minutes=5), 
    )

    # hybrid inference
    t2 = PythonOperator(
        task_id="batch_inference_by_hybrid", 
        python_callable=batch_inference, 
        depends_on_past=False, 
        owner="judy",
        retries=3,
        retry_delay=timedelta(minutes=5), 
    )

    # save results
    t3 = PythonOperator(
        task_id="save_results", 
        python_callable=save_results, 
        depends_on_past=False, 
        owner="judy",
        retries=3,
        op_kwargs={
            'collection_name': 'model_recommendation_history_hybrid', 
            'meta': {'model_version': '0.0.1'}},
        retry_delay=timedelta(minutes=5), 
    )

    t1 >> t2 >> t3
