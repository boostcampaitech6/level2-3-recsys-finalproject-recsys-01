import argparse
from datetime import datetime as dt
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


def recipe_info(recipe_id, driver):

    recipe_data = {
        "recipe_id": 0,
        "recipe_name": None,
        "author_id": None,
        "author_name": None,
        "ingredient": None,
        "time_taken": None,
        "difficulty": None,
        "recipe_url": None,
        "portion": None,
        "food_img_url": None,
        "reviews": 0,
        "photo_reviews": 0,
        "comments": 0,
        "datePublished": None,
    }
    
    try:
        recipe_data["recipe_id"] = recipe_id
        recipe_data["recipe_url"] = f"https://www.10000recipe.com/recipe/{recipe_id}"
        driver.get(recipe_data["recipe_url"])
        time.sleep(3)
        close_popup(driver)
        driver.maximize_window()
        # 페이지가 로드될 때까지 대기
        
        try:
            recipe_info = driver.find_element(
                By.XPATH, "//script[@type='application/ld+json']"
            )
            recipe_txt = json.loads(recipe_info.get_attribute("innerHTML"))
            # 작성자 id 가져오기
            author_elem = driver.find_element(By.CLASS_NAME, "user_info2")
            author_aTag = author_elem.find_elements(By.TAG_NAME, "a")[0]
            href = author_aTag.get_attribute("href")
            try:
                recipe_data["author_id"] = href.split("uid=")[1]
            except:
                recipe_data["author_id"] = href.split("cid=")[1]
                pass

            #breakpoint()
            # 레시피 관련 요약 정보
            try:
                recipe_data["portion"] = driver.find_element(
                    By.CLASS_NAME, "view2_summary_info1"
                ).text  # recipe_txt['recipeYield']
            except:
                pass

            try:
                recipe_data["time_taken"] = driver.find_element(
                    By.CLASS_NAME, "view2_summary_info2"
                ).text  # recipe_txt['totalTime']
            except:
                pass
            try:
                recipe_data["difficulty"] = driver.find_element(By.CLASS_NAME, "view2_summary_info3").text
            except:
                pass

            # 요리 후기 수
            recipe_data["recipe_name"] = recipe_txt["name"]
            recipe_data["author_name"] = recipe_txt["author"]["name"]
            recipe_data["food_img_url"] = recipe_txt["image"][1]
            recipe_data["datePublished"] = recipe_txt["datePublished"]
            
            # 재료
            try:
                recipe_data["ingredient"] = recipe_txt["recipeIngredient"]
            except KeyError:
                try:
                    ingredient_elems = driver.find_elements(By.TAG_NAME, "dd")
                    ingredient_lst = []
                    for elem in ingredient_elems:
                        if len(elem.text.split(" ")):
                            ingredient_lst.append(elem.text)

                    recipe_data["ingredient"] = ingredient_lst  # KeyError
                except Exception as e:
                    #print(">>>> KeyError + a :", recipe_id)
                    #breakpoint()
                    print(recipe_id, e)
                    pass
                pass

            # 리뷰, 포토 리뷰, 댓글
            try:
                # print('>>> pdb')
                # breakpoint()
                reviews_cnt_elems = driver.find_elements(By.ID, "recipeCommentListCount")
                for reviews_cnt_elem in reviews_cnt_elems:
                    driver.execute_script("arguments[0].scrollIntoView();", reviews_cnt_elem)
                    what_text = reviews_cnt_elem.find_element(By.XPATH, "..").text.split(" ")[0]
                    what_cnt = int(reviews_cnt_elem.text)

                    if what_text == "요리":
                        recipe_data["reviews"] = what_cnt
                    elif what_text == "포토":
                        recipe_data["photo_reviews"] = what_cnt
                    elif what_text == "댓글":
                        recipe_data["comments"] = what_cnt
            except Exception as e:
                #print(">>> reviews X") # recipe_id : 6909808
                #breakpoint()
                print(recipe_id, e)
                pass
        except Exception as e:
            #print(">>> recipe_info X")
            #breakpoint() # 6909824, 6910570, 6910581, 6911221, 6911538
            print(recipe_id, e)
            pass

    except Exception as e:
        #print(">>> recipe_id: ", recipe_data["recipe_id"]) # 6910133
        #breakpoint()
        print(recipe_id, e)
        pass

    return recipe_data


def main(args):
    service = ChromeService(executable_path=r'/usr/bin/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    
    df = pd.read_csv(
        args.data_path, encoding="cp949", low_memory=False, encoding_errors="ignore"
    )

    recipe_data_lst = []
    for idx, row in tqdm(df.iterrows()):

        recipe_id = row["RCP_SNO"]
        recipe_data = recipe_info(recipe_id, driver)
        recipe_data_lst.append(recipe_data)

        if idx % 1000 == 0:
            new_recipe_data = pd.DataFrame(recipe_data_lst)
            save_recipe_results(args.save_path, new_recipe_data)
            print(" >>> Saved:", args.save_path, idx)
            recipe_data_lst = []

    #breakpoint()
    if recipe_data_lst != []:
        new_recipe_data = pd.DataFrame(recipe_data_lst)
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
        "--webdriver_path",
        type=str,
        default="chromedriver.exe",
        help="Chromedriver path를 설정할 수 있습니다.",
    )

    args = parser.parse_args()
    main(args)
