import re, os
from datetime import datetime as dt

import numpy as np
import pandas as pd
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException

from bs4 import BeautifulSoup

def get_userid_from_recipe_reviews():

    # filenames
    crawled_files = [
        'reviewers_240309.csv'
    ]

    df = pd.concat([pd.read_csv(f) for f in crawled_files], axis=0)
    unique_users = set(np.concatenate(df['reviewers'].apply(eval).values))
    
    return unique_users

def get_userid_set():
    # filenames
    RECIPE_FILE1 = 'TB_RECIPE_SEARCH-220701.csv'
    RECIPE_FILE2 = 'TB_RECIPE_SEARCH-20231130.csv'

    # read file
    recipe_df_22 = pd.read_csv(RECIPE_FILE1, engine='python', encoding='cp949', encoding_errors='ignore') # EUC-KR, utf-8, cp949, ms949, iso2022_jp_2, iso2022_kr johab
    recipe_df_23 = pd.read_csv(RECIPE_FILE2, engine='python', encoding='cp949', encoding_errors='ignore')

    # union recipes
    recipeset_22 = set(recipe_df_22['RGTR_ID'].values)
    recipeset_23 = set(recipe_df_23['RGTR_ID'].values)
    recipeset_all = recipeset_22 | recipeset_23

    print(len(recipeset_22), len(recipeset_23), len(recipeset_all))
    return recipeset_all

def get_html_source(driver, uid:str='pingky7080', page_no=1):
    url = f'https://m.10000recipe.com/profile/recipe.html?uid={uid}&page={page_no}'
    driver.get(url) # url 접속
    driver.implicitly_wait(3)

    return driver.page_source

def parse_user_recipes(soup):
    user_recipes = list()
    for recipe in soup.find('div', 'recipe_list').find_all('div', 'media'):
        recipe_id = parse_recipe_id(recipe)
        if len(recipe_id) <= 0: continue 
        user_recipes.append(recipe_id)

    return user_recipes

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

def save_results(data_list):

    # build df
    df = pd.DataFrame(data_list)
    date = dt.now().strftime('%y%m%d')

    PATH = f'recipes_{date}.csv'
    if os.path.exists(PATH):
        # save
        df.to_csv(PATH, mode='a', index=False, header=False)
    else:
        df.to_csv(PATH, index=False)


def main():
    # get all user ids
    # recipeid_set = get_userid_set()
    recipeid_set = get_userid_from_recipe_reviews()

    # set options for opening chrome browser in CLI env
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # headless 모드로 실행

    # get automative driver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')  # sandbox를 사용하지 않는다는 옵션!! 필수
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=options)
    
    # collect data by user id
    for i,uid in enumerate(tqdm(recipeid_set)):
        try:
            html_source = get_html_source(driver, uid)
            soup = BeautifulSoup(html_source, 'html.parser')
            
            # total recipe count for pagination
            num_recipe = soup.find('div', 'myhome_cont').find('li', 'active').find('p', 'num').text
            num_recipe = re.sub(r'\D', '', num_recipe) # 숫자 아닌 값 제거; decimal point(,) 제거
            num_recipe = int(num_recipe)
            
            next_page_num: int = num_recipe // 20
            user_recipes = list()
            user_recipes.extend(parse_user_recipes(soup))

            for page_no in range(2, next_page_num+2):
                # parsing
                next_page_source = get_html_source(driver, uid, page_no)
                soup = BeautifulSoup(next_page_source, 'html.parser')

                # parse review by recipes
                user_recipes.extend(parse_user_recipes(soup))
    
            if len(user_recipes) > 0:
                save_results([{
                    'uid': uid,
                    'recipes': user_recipes,
                }])
        except KeyboardInterrupt:
            break
        except:
            continue


if __name__ == '__main__':
    main()
