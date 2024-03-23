import re

import pendulum
from datetime import datetime as dt
from datetime import timedelta, date
from pymongo import MongoClient
from pymongo.collection import Collection

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from db_config import db_host, db_port

from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

from tqdm import tqdm

class Interaction:
    def __init__(self, client: MongoClient, database: str):
        self.trarin_inter_collection: Collection = client[f'{database}']['train_inter']
        self.train_user_collection: Collection = client[f'{database}']['train_users']
        self.recipe_collection: Collection = client[f'{database}']['recipes']

    def crawl(self, target_date: date):
        return self._review_crawl(target_date=target_date), self._recipe_crawl()

    def _recipe_crawl(self):
        return {
            'user_count': 0,
            'interaction_count': 0
        }

    def _review_crawl(self, target_date: date):
        # get automative driver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        
        user_count, interaction_count = 0, 0

        for uid in tqdm(self._user_uids()):
            try:
                html_source = Interaction.get_html_source(driver, uid) # temporarily fixed
                soup = BeautifulSoup(html_source, 'html.parser')

                # parse review by recipes
                user_history = list()
                for review in soup.find('ul', id='listDiv').find_all('div', 'media'):
                    recipe_id = Interaction.parse_recipe_id(review)
                    if recipe_id == '': continue 
                    
                    rating = len(review.find('span', 'view2_review_star').find_all('img'))
                    datetime = review.find('span', {'style': "font-size:11px;color:#888;display: block; padding-top: 4px;"}).text
                    datetime = dt.strptime(datetime, "%Y-%m-%d %H:%M")
                    
                    if target_date == datetime.date():
                        user_history.append({'uid': uid, 'sno': recipe_id, 'rating': rating, 'datetime': datetime})

                if len(user_history) > 0:
                    self.trarin_inter_collection.insert_many(user_history)
                    interaction_count += len(user_history)
                
                user_count += 1
            except KeyboardInterrupt:
                break

        return {
            'user_count': user_count,
            'interaction_count': interaction_count
        }
            
    @staticmethod
    def get_html_source(driver, uid:str):
        url = f'https://m.10000recipe.com/profile/review.html?uid={uid}'
        print(url)
        driver.get(url) # url 접속
        driver.implicitly_wait(2)

        # 후기 수// 10 만큼 더보기 버튼 누르기
        num_review = int(driver.find_element(By.CLASS_NAME, 'myhome_cont').find_element(By.CLASS_NAME, 'active').find_element(By.CLASS_NAME, 'num').text)

        for i in range(num_review//10):
            btn_href = driver.find_elements(By.CLASS_NAME, 'view_btn_more')[-1].find_element(By.TAG_NAME, 'a')
            driver.execute_script("arguments[0].click();", btn_href) #자바 명령어 실행
            driver.implicitly_wait(2)

        # 페이지의 HTML 소스 가져오기
        return driver.page_source
    
    @staticmethod
    def parse_recipe_id(review):
        recipe_id = ''
        onclick_attr = review.get('onclick')
        if onclick_attr:
            match = re.search(r"location.href='([^']+)'", onclick_attr)
            if match:
                # URL 출력
                url = match.group(1)
                recipe_id = url.split('/')[-1]
        return recipe_id
    
    def _user_uids(self, limit: int=10):
        return [user['uid'] for user in self.train_user_collection.find().sort({'uid':1}).limit(limit)]

def crawl_interaction(**kwargs):
    execution_date = kwargs.get('execution_date')
    print('excution date: ', execution_date)

    client = MongoClient(host=db_host, port=db_port)
    db = client.dev
    collection = db.ingredients
    print('collection', collection)

    interaction = Interaction(client=client, database='dev')

    yesterday: date = (execution_date - timedelta(days=1)).date()
    results = interaction.crawl(target_date=yesterday)

    print('[Result]:', results)

with DAG(
        dag_id="interaction_crawl",
        description="crawling new interactions once per a day at 2AM",
        start_date=pendulum.datetime(2023, 10, 18, tz="Asia/Seoul"),
        catchup=False,
        schedule_interval="0 2 * * *", # 매일 2시에 시작
        tags=["basket_recommendation", "crawling", "interaction"],
        ) as dag:

    # get active user 
    t1 = PythonOperator(
        task_id="crawl_interaction",
        python_callable=crawl_interaction,
        depends_on_past=False,
        owner="judy",
        retries=3,
        retry_delay=timedelta(minutes=5), 
    )

    t1
