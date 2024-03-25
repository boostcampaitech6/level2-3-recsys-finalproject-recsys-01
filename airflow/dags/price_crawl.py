import os, re
from datetime import datetime as dt
from datetime import timedelta
from pprint import pprint

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from airflow import DAG
from airflow.operators.python import task

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from tqdm import tqdm

from db_config import db_port, db_host


def log_exception(fname, log):
    with open(fname, 'a+') as log_file:
        log_file.write(log + "\n")

def create_upper_folder(fpath):
    folder_path = os.path.dirname(fpath)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"폴더 '{folder_path}' 생성")
        
def iso_format_time(current_time):
    return current_time.strftime("%Y-%m-%dT%H:%M")

def price2num(price_text):
    pattern = re.compile(r'\d+')
    numbers = pattern.findall(price_text)
    price = ''.join(numbers)
    return int(price)

class PriceCrawler:
    def __init__(self, id, query):
        self.id = id
        self.url = f'https://alltimeprice.com/search/?search={query}'
    
    def launch_crawler(self, driver):
        self.driver = driver
        self.driver.get(self.url)
        self.driver.implicitly_wait(3)
    
    def crawl_price(self, datetime: dt):

        elem = self.driver.find_element(By.XPATH, "//*[@id='page-content-wrapper']/div[6]/div/div[4]/div[1]")
        divs = elem.find_elements(By.XPATH, "./div")
        
        if len(divs) >= 6:
            divs = elem.find_elements(By.XPATH, "./div")[:6] # 상위 6개만
        elif len(divs) > 0:
            divs = elem.find_elements(By.XPATH, "./div")
        else:
            # 검색 결과 0개인 경우
            min_price_document = {'ingredient_id' : self.id,
                        'product_name': None,
                        'date': datetime,
                        'price_url' : None,
                        'img_url' : None,
                        'price': None}
            return min_price_document
        
        
        min_price = float('inf')
        min_price_document = None
        
        for i, div in enumerate(divs):
            
            a_tag = divs[i].find_element(By.TAG_NAME, "a")
            item_url = a_tag.get_attribute('href')
            
            img_tag = a_tag.find_element(By.TAG_NAME, 'img')
            img_url = img_tag.get_attribute('src')
            
            price_num = price2num(a_tag.find_element(By.CLASS_NAME, 'price').text)
            product_name = a_tag.find_element(By.CLASS_NAME, 'title').text
                
            new_document = {'ingredient_id' : self.id,
                        'product_name': product_name,
                        'date': datetime,
                        'price_url' : item_url,
                        'img_url' : img_url,
                        'price' : price_num,
                        }
            
            if price_num < min_price:
                min_price = price_num
                min_price_document = new_document
        
        return min_price_document


# @task(task_id='ingredients',
#       depends_on_past=False,
#       owner='charlie',
#       retries=3,
#       retry_delay=timedelta(minutes=3))
# def get_ingredients(**context):
#     client = MongoClient(host=db_host, port=db_port)
#     db = client.dev

#     return list(db['ingredients'].find({}))

@task(task_id='crawl_price',
      depends_on_past=False,
      owner='charlie',
      retries=3,
      retry_delay=timedelta(minutes=3))
def crawl_price(**context):
    
    log_path = "../logs/crawl_price/price_db_error.txt"
    create_upper_folder(log_path)
    
    # db connection
    client = MongoClient(host=db_host, port=db_port)
    db = client.dev
    new_collection = db['prices']
    
    # chrome setting
    service = ChromeService(ChromeDriverManager().install())
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-agent={user_agent}')
    driver = webdriver.Chrome(service=service, options=options)

    # execution time
    datetime: dt = context['logical_date']
    print(datetime)

    # crawling
    ingredients = list(db['ingredients'].find({}))
    print([ingredient['_id'] for ingredient in ingredients])
    for document in tqdm(ingredients):
        # crawled doc 만들기
        if document['name'] == '':
            crawled_document = {
                'ingredient_id' : document['_id'],
                'product_name': None,
                'date': datetime,
                'price_url' : None,
                'img_url' : None,
                'price': None
            }
        else:
            try:
                crawler = PriceCrawler(id = document['_id'], query=document['name'])
                crawler.launch_crawler(driver)
                crawled_document = crawler.crawl_price(datetime)
            except Exception as e:
                log_exception(log_path, str(document['_id']))
                
                crawled_document = {
                    'ingredient_id' : document['_id'],
                    'product_name': None,
                    'date': datetime,
                    'price_url' : None,
                    'img_url' : None,
                    'price': None
                }
                pass
        
        # insert 하기
        try:
            new_collection.insert_one(crawled_document)
        except DuplicateKeyError:
            try:
                new_collection.update_one({'_id': document['_id']},  {"$set": crawled_document}, upsert=True)
            except:
                log_exception(log_path, str(document['_id']))
                pass
        except KeyboardInterrupt:
            break
        except Exception as e:
            # breakpoint()
            log_exception(log_path, str(document['_id']))
            pass


with DAG(
    dag_id='price_crawl',
    description="Crawl ingredients price once per a day at 2:00AM KST",
    start_date=dt(2024,3,24),
    catchup=False,
    schedule_interval="0 2 * * *", # 매일 2시에 시작
    tags=["basket_recommendation", "crawling", "price"],
) as dag:
    
    # get_ingredient_names_task = get_ingredients()

    crawl_price_task = crawl_price()

    crawl_price_task