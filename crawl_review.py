import re
from datetime import datetime as dt

import pandas as pd
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

def get_userid_set():
    # filenames
    RECIPE_FILE1 = 'TB_RECIPE_SEARCH-220701.csv'
    RECIPE_FILE2 = 'TB_RECIPE_SEARCH-20231130.csv'

    # read file
    recipe_df_22 = pd.read_csv(RECIPE_FILE1, engine='python', encoding='cp949', encoding_errors='ignore') # EUC-KR, utf-8, cp949, ms949, iso2022_jp_2, iso2022_kr johab
    recipe_df_23 = pd.read_csv(RECIPE_FILE2, engine='python', encoding='cp949', encoding_errors='ignore')

    # union users
    userset_22 = set(recipe_df_22['RGTR_ID'].values)
    userset_23 = set(recipe_df_23['RGTR_ID'].values)
    userset_all = userset_22 | userset_23

    print(len(userset_22), len(userset_23), len(userset_all))
    return userset_all

def get_html_source(driver, uid:str=16221801):

    url = f'https://m.10000recipe.com/profile/review.html?uid={uid}'
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

    PATH = f'reviews_{date}.csv'
    
    # save
    df.to_csv(PATH)


def main():
    # get all user ids
    userid_set = get_userid_set()

    # get automative driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    # datalist 
    data_list = [] 

    # collect data by user id
    for i,uid in enumerate(tqdm(userid_set)):

        try:
            html_source = get_html_source(driver, uid) # temporarily fixed
            soup = BeautifulSoup(html_source, 'html.parser')

            nickname = soup.find('p', 'pic_r_name').text.split('\n')[0].strip()

            # parse review by recipes
            user_history = dict()
            for review in soup.find('ul', id='listDiv').find_all('div', 'media'):
                recipe_id = parse_recipe_id(review)
                if len(recipe_id) <= 0: continue 
                rating = len(review.find('span', 'view2_review_star').find_all('img'))
                user_history[recipe_id] = rating
            
            if len(user_history) > 0:
                data_list.append({
                    'uid': uid,
                    'user_name': nickname,
                    'history': user_history,
                })
        except:
            continue

    # save results
    save_results(data_list)

if __name__ == '__main__':
    main()
