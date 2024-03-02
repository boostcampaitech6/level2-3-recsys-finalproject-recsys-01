import os
from datetime import datetime as dt
from tqdm import tqdm
import pandas as pd 

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

def get_recipesno_set():
    # filenames
    RECIPE_FILE1 = 'TB_RECIPE_SEARCH-220701.csv'
    RECIPE_FILE2 = 'TB_RECIPE_SEARCH-20231130.csv'

    # read file
    recipe_df_22 = pd.read_csv(RECIPE_FILE1, engine='python', encoding='cp949', encoding_errors='ignore') # EUC-KR, utf-8, cp949, ms949, iso2022_jp_2, iso2022_kr johab
    recipe_df_23 = pd.read_csv(RECIPE_FILE2, engine='python', encoding='cp949', encoding_errors='ignore')

    # union recipes 
    recipeset_22 = set(recipe_df_22['RCP_SNO'].values)
    recipeset_23 = set(recipe_df_23['RCP_SNO'].values)
    recipeset_all = recipeset_22 | recipeset_23

    print(len(recipeset_22), len(recipeset_23), len(recipeset_all))
    return recipeset_all

def get_html_source(driver, sno:str=1785098):

    url = f'https://www.10000recipe.com/recipe/{sno}'
    driver.get(url) # url 접속
    driver.implicitly_wait(2)

    # 페이지의 HTML 소스 가져오기
    return driver.page_source

def save_results(data_list):

    # build df
    df = pd.DataFrame(data_list)
    date = dt.now().strftime('%y%m%d')

    PATH = f'reviewers_{date}.csv'
    if os.path.exists(PATH):
        # save
        df.to_csv(PATH, mode='a', index=False, header=False)
    else:
        df.to_csv(PATH, index=False)

def main():
    # get all recipe snos
    recipe_snos = get_recipesno_set()
    
    # set options for opening chrome browser in CLI env
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # headless 모드로 실행

    # get automative driver
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    # collect data by recipe snos
    for i, rsno in enumerate(tqdm(recipe_snos)):
        try:
            html_source = get_html_source(driver, rsno)
            soup = BeautifulSoup(html_source, 'html.parser')
            
            reviews = soup.find_all('div', 'view_reply st2')
            if len(reviews) == 0: continue
            reviews = reviews[1].find_all('div', 'media-left')
            recipe_reviewers = list()
            for review in reviews:
                recipe_reviewers.append(review.find('a')['href'].split('=')[-1])
            
            save_results([{
                'recipe_sno': rsno,
                'reviewers': recipe_reviewers
            }])
        except KeyboardInterrupt:
            exit()
        except:
            continue

if __name__ == '__main__':
    main()
