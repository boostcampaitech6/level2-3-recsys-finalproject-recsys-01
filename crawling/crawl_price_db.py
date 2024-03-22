import pandas as pd
import pymongo
from pymongo import MongoClient
import pprint
import argparse
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time
import os
import re
from tqdm import tqdm

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
    
    def crawl_price(self):

        elem = self.driver.find_element(By.XPATH, "//*[@id='page-content-wrapper']/div[6]/div/div[4]/div[1]")
        try:
            divs = elem.find_elements(By.XPATH, "./div")[:6] # 상위 6개만
        except:
            divs = elem.find_elements(By.XPATH, "./div")
            pass
        
        
        min_price = float('inf')
        min_price_document = None
        
        for i, div in enumerate(divs):
            
            a_tag = divs[i].find_element(By.TAG_NAME, "a")
            item_url = a_tag.get_attribute('href')
            
            img_tag = a_tag.find_element(By.TAG_NAME, 'img')
            img_url = img_tag.get_attribute('src')
            
            price_num = price2num(a_tag.find_element(By.CLASS_NAME, 'price').text)
            product_name = a_tag.find_element(By.CLASS_NAME, 'title').text
                
            new_document = {'_id' : self.id,
                        'product_name': product_name,
                        'date': iso_format_time(datetime.now()),
                        'price_url' : item_url,
                        'img_url' : img_url}
            
            if price_num < min_price:
                min_price = price_num
                min_price_document = new_document
        
        return min_price_document

def main(args):
    # MongoDB 연결 설정
    # client = MongoClient('mongodb://localhost:27017/')
    client = MongoClient(args.mongo_client)
    db = client['dev']  # 데이터베이스 선택
    collection = db['ingredients']  # 컬렉션 선택
    new_collection = db['prices']
    
    service = ChromeService(ChromeDriverManager().install())
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    
    
    cursor = collection.find()

    
    for document in tqdm(cursor):
        
        # crawled doc 만들기
        if document['name'] == '':
            crawled_document = {'_id' : document['_id'],
                        'product_name': None,
                        'date': None,
                        'price_url' : None,
                        'img_url' : None}
        else:
            try:
                crawler = PriceCrawler(id = document['_id'], query=document['name'])
                crawler.launch_crawler(driver)
                crawled_document = crawler.crawl_price()
            except:
                print('doc:', document)
                pass
        
        # insert 하기
        try:
            new_collection.insert_one(crawled_document)
        except pymongo.errors.DuplicateKeyError:
            try:
                new_collection.update_one({'_id': document['_id']},  {"$set": crawled_document}, upsert=True)
            except:
                print('doc:', document)
                print('crawled doc: ', crawled_document)
                pass
        except Exception as e:
            # breakpoint()
            print('error: ', e)
            print('doc:', document)
            print('crawled doc: ', crawled_document)
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="parser")
    arg = parser.add_argument

    arg("--mongo_client", type=str, default="mongodb://10.0.7.6:27017/")
    
    args = parser.parse_args()
    main(args)