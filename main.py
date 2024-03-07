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


def log_exception(fname, log):
    with open(fname, 'a+') as log_file:
        log_file.write(log + "\n")

class getRecipeCrawler:
    def __init__(self, recipe_id):
        self.url = f"https://www.10000recipe.com/recipe/{recipe_id}"

    def launch_crawler(self):
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )
        self.driver.get(self.url)
        self.driver.implicitly_wait(3)

    def run(self):
        self.launch_crawler()
        self.find_recipe()


def close_popup(driver):
    try:
        close_btn = driver.find_element(By.XPATH, "//*[@id='popup_goods']/a")
        close_btn.click()
    except Exception as e:
        pass


def get_uid_from_elem(elem):
    href = elem.get_attribute("href")
    uid = href.split("uid=")[1]
    return uid


def save_recipe_results(fpath, data):

    df = pd.DataFrame(data)
    if os.path.exists(fpath):
        df.to_csv(fpath, mode="a", index=False, header=False)
    else:
        df.to_csv(fpath, index=False)


def update_list(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    list1[:] = list(set1.union(set2))
    return list1

def create_upper_folder(fpath):
    folder_path = os.path.dirname(fpath)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"폴더 '{folder_path}' 생성")
        

def recipe_info(args, row, driver):
    
    recipe_data = {
        "recipe_id": None,
        "recipe_title" : None,
        "recipe_name": None,
        "author_id": None,
        "author_name": None,
        "recipe_method" : None,
        "recipe_status" : None,
        "recipe_kind" : None,
        "time_taken": None,
        "difficulty": None,
        "recipe_url": None,
        "portion": None,
        "datePublished": None,
        "food_img_url": None,
        "ingredient": {},
        "reviews": 0,
        "photo_reviews": 0,
        "comments": 0,
    }
    
    
    recipe_id = row['RCP_SNO']
    
    recipe_data['recipe_id'] = recipe_id
    recipe_data['recipe_title'] = row['RCP_TTL']
    recipe_data['recipe_name'] = row['CKG_NM']
    recipe_data['author_id'] = row['RGTR_ID']
    recipe_data['author_name'] = row['RGTR_NM']
    recipe_data['recipe_method']  = row['CKG_MTH_ACTO_NM']
    recipe_data['recipe_status']  = row['CKG_STA_ACTO_NM']
    recipe_data['recipe_kind']  = row['CKG_KND_ACTO_NM']
    recipe_data['time_taken'] = row['CKG_TIME_NM']
    recipe_data['difficulty'] = row['CKG_DODF_NM']
    recipe_data['recipe_url'] = f"https://www.10000recipe.com/recipe/{str(recipe_id)}"
    recipe_data['portion'] = row['CKG_INBUN_NM']
    recipe_data['datePublished'] = row['FIRST_REG_DT']

    try:
        driver.get(recipe_data["recipe_url"])
        time.sleep(3)
        close_popup(driver)
    except:
        log_exception(args.log_path, str(recipe_id))
        pass
        
    # 사진 url
    try:
        img_elem= driver.find_element(By.ID, 'main_thumbs')
        img_url = img_elem.get_attribute('src')
        recipe_data['food_img_url'] = img_url
    except:
        log_exception(args.log_path, str(recipe_id))
        pass
        
    # 재료
    try:
        ingredients_data = {}
        ingredient_elem = driver.find_element(By.ID, 'divConfirmedMaterialArea')
        ingredient_uls = ingredient_elem.find_elements(By.TAG_NAME, "ul")
        
        for ingredient_ul in ingredient_uls:
            driver.execute_script("arguments[0].scrollIntoView();", ingredient_ul)
            
            b_tag = ingredient_ul.find_element(By.TAG_NAME, 'b')
            b_tag_text = b_tag.text.strip("[]")
            
            li_tags = ingredient_ul.find_elements(By.TAG_NAME, 'li')
            
            ingredient_data_lst = []
            for li_tag in li_tags:
                ingredient_data= {'name': None, 'amount' : None}
                ingredient_name = li_tag.find_elements(By.TAG_NAME, 'a')[0].text
                ingredient_amount = li_tag.find_element(By.CLASS_NAME, 'ingre_unit').text
                ingredient_data['name'] = ingredient_name
                ingredient_data['amount'] = ingredient_amount
                
                ingredient_data_lst.append(ingredient_data)
            ingredients_data[b_tag_text] = ingredient_data_lst
        recipe_data["ingredient"] = str(ingredients_data)
    except:
        try:
            recipe_data['ingredient']  = row['CKG_MTRL_CN']
        except:
            log_exception(args.log_path, str(recipe_id))
            pass
        pass

    # 리뷰, 포토 리뷰, 댓글
    try:
        reviews_cnt_elems = driver.find_elements(By.CLASS_NAME, "view_reply")
        for reviews_cnt_elem in reviews_cnt_elems:
            driver.execute_script("arguments[0].scrollIntoView();", reviews_cnt_elem)
            title_elem = reviews_cnt_elem.find_element(By.CLASS_NAME, "reply_tit")
            title_text = title_elem.text.split(" ")[0]
            cnt_elem = reviews_cnt_elem.find_element(By.TAG_NAME, "span")
            cnt_int = int(cnt_elem.text)

            if title_text == "포토":
                recipe_data["photo_reviews"] = cnt_int
            elif title_text == "요리":
                recipe_data["reviews"] = cnt_int
            elif title_text == "댓글":
                recipe_data["comments"] = cnt_int
    except:
        log_exception(args.log_path, str(recipe_id))
        pass

    return recipe_data



def main(args):
    
    create_upper_folder(args.save_path)
    create_upper_folder(args.log_path)

    if args.chrome_install :
        service = ChromeService(ChromeDriverManager().install())
    else:
        service = ChromeService(executable_path=r'/usr/bin/chromedriver')
    
    if args.test:
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=service, options=options)

    df = pd.read_csv(
        args.data_path
    )
    
    for idx, row in tqdm(df.iterrows()):

        recipe_data = recipe_info(args, row, driver)
        new_recipe_data = pd.DataFrame([recipe_data])
        save_recipe_results(args.save_path, new_recipe_data)

    driver.quit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="parser")
    arg = parser.add_argument

    arg(
        "--data_path",
        type=str,
        default="data/split/TB_RECIPE_SEARCH-20231130_0.csv",
        help="Data path를 설정할 수 있습니다.",
    )
    arg(
        "--save_path",
        type=str,
        default="save/split/recipe_data_0.csv",
        help="Save path를 설정할 수 있습니다.",
    )
    arg(
        "--log_path",
        type=str,
        default="log/split/recipe_data_0.txt",
        help="Save path를 설정할 수 있습니다.",
    )
    
    arg(
        "--webdriver_path",
        type=str,
        default="chromedriver.exe",
        help="Chromedriver path를 설정할 수 있습니다.",
    )
    
    arg(
        "--test",
        type=bool,
        default=False,
        help="test 여부를 설정할 수 있습니다.",
    )
    
    arg("--chrome_install",
        type=bool,
        default=True,
        help="Chrome Driver Manager 로 설치 여부를 설정할 수 있습니다.")

    args = parser.parse_args()
    main(args)
