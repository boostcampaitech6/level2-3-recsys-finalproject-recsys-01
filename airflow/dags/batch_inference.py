from pymongo import MongoClient

from datetime import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from recbole_inference import inference 
from db_config import db_host, db_port

def get_active_users(**context):
    client = MongoClient(host=db_host, port=db_port)
    db = client.dev
    active_users = [user['login_id'] for user in db['users'].find()]
    print(active_users)

    user_ids = ['76017883', '94541740']
    context["ti"].xcom_push(key='user_ids', value=user_ids)

def batch_inference(**context):
    # user_ids
    user_ids = context["ti"].xcom_pull(key='user_ids')

    # 설정 파일과 모델 저장 경로 설정
    config_file_path = '/home/judy/train_model/recipe-dataset.yaml'  # 설정 파일 경로
    model_file_path = '/home/judy/train_model/saved/MultiDAE-Mar-14-2024_23-15-20.pth'  # 모델 파일 경로

    recommended_items = inference(
        user_ids=user_ids,
        modelname='MultiDAE', 
        config_file=config_file_path, 
        model_file_path=model_file_path, 
        k=20)

    context["ti"].xcom_push(key='recommended_items', value=recommended_items)

def save_results(**context):
    user_ids = context["ti"].xcom_pull(key='user_ids')
    recommended_items = context["ti"].xcom_pull(key='recommended_items')

    client = MongoClient(host=db_host, port=db_port)
    db = client.dev
    data = [{
        'id': user_id, 
        'recommended_item': recommended_item, 
        'recommended_proba': recommended_proba, 
        'date': dt.now()
        } for user_id, recommended_item, recommended_proba in zip(user_ids, recommended_items['item_ids'], recommended_items['item_proba'])] 

    db['model_recommendation_histories'].insert_many(data)
    print('push data into db')

with DAG(
        dag_id="batch_inference",
        description="batch inference of all active users using MultiDAE",
        start_date=days_ago(5), # DAG 정의 기준 2일 전부터 시작합니다. 
        schedule_interval="0 2 * * *", # 매일 2시에 시작
        tags=["basket_recommendation", "inference"],
        ) as dag:

    # get active user 
    t1 = PythonOperator(
        task_id="get_active_users", 
        python_callable=get_active_users, 
        depends_on_past=False, 
        owner="judy",
        retries=3,
        retry_delay=timedelta(minutes=5), 
    )

    # inference
    t2 = PythonOperator(
        task_id="batch_inference", 
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
        retry_delay=timedelta(minutes=5), 
    )

    t1 >> t2 >> t3
