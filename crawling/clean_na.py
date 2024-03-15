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


def save_updated_recipe_results(fpath, df):

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
                try:
                    ingredient_amount = li_tag.find_element(By.CLASS_NAME, 'ingre_unit').text
                except:
                    ingredient_amount = li_tag.find_element(By.CLASS_NAME, 'ingre_list_ea').text
                    
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


def update_recipe_info(args, row, driver):
    recipe_data = {
        "recipe_id": row['recipe_id'],
        "recipe_title" : row['recipe_title'],
        "recipe_name": row['recipe_name'],
        "author_id": row['author_id'],
        "author_name": row['author_name'],
        "recipe_method" : row['recipe_method'],
        "recipe_status" : row['recipe_status'],
        "recipe_kind" : row['recipe_kind'],
        "time_taken": row['time_taken'],
        "difficulty": row['difficulty'],
        "recipe_url": row['recipe_url'],
        "portion": row['portion'],
        "datePublished": row['datePublished'],
        "food_img_url": row['food_img_url'],
        "ingredient": {},
        "reviews": row['reviews'],
        "photo_reviews": row['photo_reviews'],
        "comments": row['comments'],
    }
    
    
    recipe_id = recipe_data['recipe_id']
    
    try:
        driver.get(recipe_data["recipe_url"])
        driver.implicitly_wait(3)
        close_popup(driver)
    except:
        log_exception(args.log_path, str(recipe_id))
        pass
        
    # 재료
    
    
    try:
        # 원래
        ingredients_data = {}
        ingredient_elem = driver.find_element(By.ID, 'divConfirmedMaterialArea')
        ingredient_uls = ingredient_elem.find_elements(By.TAG_NAME, "ul")
        
        for ingredient_ul in ingredient_uls:
            driver.execute_script("arguments[0].scrollIntoView();", ingredient_ul)
            
            b_tag = ingredient_ul.find_element(By.TAG_NAME, 'b')
            b_tag_text = b_tag.text.strip("[]")
            
            li_tags = ingredient_ul.find_elements(By.TAG_NAME, 'li')
            
            ingredient_data_lst = []
            #breakpoint()
            for li_tag in li_tags:
                ingredient_data= {'name': None, 'amount' : None}
                
                
                try:
                    ingredient_name = li_tag.find_element(By.CLASS_NAME, 'ingre_list_name').text
                except:
                    log_exception(args.log_path, str(recipe_id))
                    print(recipe_data['recipe_url'])
                    breakpoint()
                
                try:
                    ingredient_amount = li_tag.find_element(By.CLASS_NAME, 'ingre_unit').text
                except:
                    ingredient_amount = li_tag.find_element(By.CLASS_NAME, 'ingre_list_ea').text
                ingredient_data['name'] = ingredient_name
                ingredient_data['amount'] = ingredient_amount
                
                ingredient_data_lst.append(ingredient_data)
            ingredients_data[b_tag_text] = ingredient_data_lst
        recipe_data["ingredient"] = str(ingredients_data)
    except:
        try:
        
            ingredient_elem = driver.find_element(By.CLASS_NAME, 'cont_ingre')
            ingredient_dls = ingredient_elem.find_elements(By.TAG_NAME, "dl")
            ingredients_data = {}
            
            for ingredient_dl in ingredient_dls:
                ingredient_text = ingredient_dl.text
                pattern = r'\[([^]]+)\]\n(.*)'
                matches = re.findall(pattern, ingredient_text)

                for category, ingredients_text in matches:
                    ingredients_list = ingredients_text.split(',')
                    parsed_ingredients = []
                    for ingredient in ingredients_list:
                        pattern2 = r'(\D+)(\d.*\d*)(\D+)'
                        matches = re.match(pattern2, ingredient)
                        if matches:
                            name = matches.group(1).strip()
                            if ']' in name:
                                name = name.split(']')[1].strip(' ')
                            amount = matches.group(2).strip()
                            unit = matches.group(3).strip()
                            parsed_ingredients.append({'name': name, 'amount': amount + unit})      
                        else:
                            ingredient = ingredient.strip(' ')
                            parsed_ingredients.append({'name': ingredient, 'amount': None})   
                            
                            
                    ingredients_data[category] = parsed_ingredients
            recipe_data['ingredient'] = str(ingredients_data)
        except:
                
            log_exception(args.log_path, str(recipe_id))
            print(recipe_data['recipe_url'])
            breakpoint()
            pass
        
        
    return recipe_data


def main(args):
    
    create_upper_folder(args.save_path)
    create_upper_folder(args.log_path)

    service = ChromeService(ChromeDriverManager().install())
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)

    df = pd.read_csv(args.data_path)
    df = df.drop(columns = ['flag'])
    
    
    for idx, row in tqdm(df.iterrows()):
        updated_data = update_recipe_info(args, row, driver)
        save_recipe_results(args.save_path, [updated_data])

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

    args = parser.parse_args()
    main(args)
