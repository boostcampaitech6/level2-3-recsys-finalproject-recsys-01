from datetime import datetime as dt

from tqdm import tqdm
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException

from bs4 import BeautifulSoup

def get_html_source(driver, rank_standard:str='r', period:str='d'):

    url = f"https://www.10000recipe.com/ranking/home_new.html?dtype={period}&rtype={rank_standard}"
    driver.get(url) # url 접속
    driver.implicitly_wait(2)

    return driver.page_source

def main():
    # chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')  # sandbox를 사용하지 않는다는 옵션!! 필수
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=options)
    
    # only ranked recipes
    # for 주간 월간 일간
    crawled_ids = []

    rank_standard = 'c'
    for period in ['d', 'w', 'm']:

        # 레시피 랭킹 페이지 읽어
        html_source = get_html_source(driver, rank_standard=rank_standard, period=period)

        # make soup obj
        soup = BeautifulSoup(html_source, 'html.parser')

        # parse recipe snos
        if rank_standard == 'r':
            ## <div class="common_sp_thumb">
            ## <a href="/recipe/1785098" class="common_sp_link">
            for items in tqdm(soup.find_all('li', 'common_sp_list_li')):
                crawled_id = items.find('div', 'common_sp_thumb').find('a', 'common_sp_link').get('href').split('/')[-1]
                crawled_ids.append(crawled_id)
        elif rank_standard == 'c':
            ## ul class="goods_best4_1"
            ## div class="best_pic"
            ## a href="/profile/index.html?uid=minimini0107"
            for items in tqdm(soup.find('ul', 'goods_best4_1').find_all('li')):
                crawled_id = items.find('div', 'best_pic').find('a').get('href').split('uid=')[-1]
                crawled_ids.append(crawled_id)

    # numpy 로 저장
    if rank_standard == 'r':
        crawled_ids = np.unique(np.array(crawled_ids))
        filename = f'ranked_recipe_snos-{dt.now().strftime("%y%m%d")}.npy'
    elif rank_standard == 'c':
        crawled_ids = np.unique(np.array(crawled_ids))
        filename = f'ranked_chef_uids-{dt.now().strftime("%y%m%d")}.npy'

    np.save(filename, crawled_ids)
    

if __name__ == '__main__':
    main()
