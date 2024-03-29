from datetime import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from db_operations import fetch_user_histories, update_model_recommendations, cb_inference, blending_results
from recbole_inference import sasrec_inference 

def fetch_and_push_user_histories(result_type:str=None, **context):
    if result_type:
        user_id_and_feedbacks = fetch_user_histories(result_type)
        context["ti"].xcom_push(key='user_id_and_feedbacks_cb', value=user_id_and_feedbacks)
    else:
        user_id_and_feedbacks = fetch_user_histories()
        context["ti"].xcom_push(key='user_id_and_feedbacks_hybrid', value=user_id_and_feedbacks)

def hybrid_inference(**context):
    user_id_and_feedbacks = context["ti"].xcom_pull(key='user_id_and_feedbacks_hybrid')

    # 설정 파일과 모델 저장 경로 설정
    modelpath = '/home/judy/level2-3-recsys-finalproject-recsys-01/ml/Sequential/saved/SASRec-Mar-25-2024_03-39-27.pth'

    recommended_results = sasrec_inference(
        modelpath, 
        user_id_and_feedbacks)

    context["ti"].xcom_push(key='hybrid_recommended_results', value=recommended_results)

def save_results_hybrid(collection_name, **context):
    recommended_results = context["ti"].xcom_pull(key='hybrid_recommended_results')
    update_model_recommendations(recommended_results, collection_name)

def cb_inference_(**context):
    user_id_and_feedbacks = context["ti"].xcom_pull(key='user_id_and_feedbacks_cb')

    recommended_results = cb_inference(
        user_id_and_feedbacks)

    context["ti"].xcom_push(key='cb_recommended_results', value=recommended_results)

def save_results_cb(collection_name, input_type, **context):
    recommended_results = context["ti"].xcom_pull(key='cb_recommended_results')
    update_model_recommendations(recommended_results, collection_name, input_type=input_type)

def blending_results_(**context):
    hybrid_recommended_results = context["ti"].xcom_pull(key='hybrid_recommended_results')
    cb_recommended_results = context["ti"].xcom_pull(key='cb_recommended_results')

    blended_results = blending_results(hybrid_recommended_results, cb_recommended_results)

    context["ti"].xcom_push(key='blended_recommended_results', value=blended_results)

def save_results_blended(collection_name, input_type, **context):
    recommended_results = context["ti"].xcom_pull(key='blended_recommended_results')
    update_model_recommendations(recommended_results, collection_name, input_type=input_type)

with DAG(
        dag_id="batch_inference",
        description="batch inference of all active users using BERT4Rec",
        start_date=days_ago(5), # DAG 정의 기준 2일 전부터 시작합니다. 
        schedule_interval="0 2 * * *", # 매일 2시에 시작
        tags=["basket_recommendation", "inference"],
        ) as dag:

    # get active user 
    t1 = PythonOperator(
        task_id="fetch_and_push_user_histories_for_hybrid",
        python_callable=fetch_and_push_user_histories,
        depends_on_past=False, 
        owner="judy",
        retries=3,
        retry_delay=timedelta(minutes=5), 
    )

    # hybrid inference
    t2 = PythonOperator(
        task_id="batch_inference_by_hybrid", 
        python_callable=hybrid_inference, 
        depends_on_past=False, 
        owner="judy",
        retries=3,
        retry_delay=timedelta(minutes=5), 
    )

    # save results1
    t3 = PythonOperator(
        task_id="save_results_hybrid", 
        python_callable=save_results_hybrid, 
        depends_on_past=False, 
        owner="judy",
        retries=3,
        op_kwargs={
            'collection_name': 'model_recommendation_history_hybrid', 
            'meta': {'model_version': '0.0.1'}},
        retry_delay=timedelta(minutes=5), 
    )

    # get active user 
    t4 = PythonOperator(
        task_id="fetch_and_push_user_histories_for_cb",
        python_callable=fetch_and_push_user_histories,
        depends_on_past=False, 
        owner="judy",
        retries=3,
        op_kwargs={
            'result_type': 'recipe_id', 
            },
        retry_delay=timedelta(minutes=5), 
    )

    # content-based inference
    t5 = PythonOperator(
        task_id="batch_inference_by_content_based", 
        python_callable=cb_inference_, 
        depends_on_past=False, 
        owner="judy",
        retries=3,
        retry_delay=timedelta(minutes=5), 
    )

    # save results2
    t6 = PythonOperator(
        task_id="save_results_cb", 
        python_callable=save_results_cb, 
        depends_on_past=False, 
        owner="judy",
        retries=3,
        op_kwargs={
            'collection_name': 'model_recommendation_history_cb', 
            'input_type': 'recipe_id', 
            },
        retry_delay=timedelta(minutes=5), 
    )

    # content-based inference
    t7 = PythonOperator(
        task_id="blending_results", 
        python_callable=blending_results_, 
        depends_on_past=False, 
        owner="judy",
        retries=3,
        retry_delay=timedelta(minutes=5), 
    )

    # save results3
    t8 = PythonOperator(
        task_id="save_results_blended", 
        python_callable=save_results_blended, 
        depends_on_past=False, 
        owner="judy",
        retries=3,
        op_kwargs={
            'collection_name': 'model_recommendation_history_total', 
            'input_type': 'recipe_id', 
            },
        retry_delay=timedelta(minutes=5), 
    )
    t1 >> t2
    t4 >> t5
    [t2, t5] >> t7 >> t8
    t2 >> t3
    t5 >> t6
