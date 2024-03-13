import re, os
from datetime import datetime as dt

import pandas as pd
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException

from bs4 import BeautifulSoup


def get_html_source(driver, name):
    url = f'https://alltimeprice.com/search/?search={name}'
    driver.get(url) # url 접속
    driver.implicitly_wait(3)

    return driver.page_source


def save_results(data_list):

    # build df
    df = pd.DataFrame(data_list)
    date = dt.now().strftime('%y%m%d')

    PATH = f'prices_{date}.csv'
    if os.path.exists(PATH):
        # save
        df.to_csv(PATH, mode='a', index=False, header=False)
    else:
        df.to_csv(PATH, index=False)


def main():

    # set options for opening chrome browser in CLI env
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # headless 모드로 실행

    # get automative driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    # collect data by food name
    food_set = set(['식빵', '봄동'])
    for i, name in enumerate(tqdm(food_set)):
        try:
            html_source = get_html_source(driver, name)
            soup = BeautifulSoup(html_source, 'html.parser')

            print(soup)
            prices = soup.findAll('p', 'price')
            print(prices)
            if len(prices) > 0:
                first_price = re.sub(r'\D', '', prices[0].text) # 숫자 아닌 값 제거; decimal point(,) 제거

                save_results([{
                    'name': name,
                    'price': first_price,
                }])
        except UnexpectedAlertPresentException:
            continue

if __name__ == '__main__':
    main()
