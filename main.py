import argparse
from datetime import datetime as dt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

import json
import time
import os
import re
from tqdm import tqdm


# TODO
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

    def close_popup(self):
        try:
            close_btn = self.driver.find_element(By.XPATH, "//*[@id='popup_goods']/a")
            close_btn.click()
        except:
            pass


def close_popup(driver):
    try:
        close_btn = driver.find_element(By.XPATH, "//*[@id='popup_goods']/a")
        close_btn.click()
    except:
        pass


def get_uid_from_elem(elem):
    href = elem.get_attribute("href")
    uid = href.split("uid=")[1]
    return uid


def save_recipe_results(fname, data):
    df = pd.DataFrame(data)

    PATH = f"save/{fname}.csv"
    if os.path.exists(PATH):
        df.to_csv(PATH, mode="a", index=False, header=False)
    else:
        df.to_csv(PATH, index=False)


def save_uid_results(fname, data):

    df = pd.DataFrame(data, columns=["user_id"])

    PATH = f"save/{fname}.csv"
    if os.path.exists(PATH):
        df.to_csv(PATH, mode="a", index=False, header=False)
    else:
        df.to_csv(PATH, index=False)


def update_list(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    list1[:] = list(set1.union(set2))
    return list1


def recipe_info(recipe_id, driver):
    recipe_df = None

    url = f"https://www.10000recipe.com/recipe/{recipe_id}"
    driver.get(url)
    time.sleep(3)
    close_popup(driver)
    driver.maximize_window()

    close_popup(driver)

    try:
        recipe_info = driver.find_element(
            By.XPATH, "//script[@type='application/ld+json']"
        )
        recipe_txt = json.loads(recipe_info.get_attribute("innerHTML"))

    except Exception as e:
        print("Error : Start")

    # 작성자 id 가져오기
    author_elem = driver.find_element(By.CLASS_NAME, "user_info2")
    author_aTag = author_elem.find_elements(By.TAG_NAME, "a")[0]
    href = author_aTag.get_attribute("href")
    author_id = href.split("uid=")[1]

    # 레시피 관련 요약 정보
    try:
        summary1 = driver.find_element(
            By.CLASS_NAME, "view2_summary_info1"
        ).text  # recipe_txt['recipeYield']
    except:
        summary1 = None
        pass

    try:
        summary2 = driver.find_element(
            By.CLASS_NAME, "view2_summary_info2"
        ).text  # recipe_txt['totalTime']
    except:
        summary2 = None
        pass

    try:
        summary3 = driver.find_element(By.CLASS_NAME, "view2_summary_info3").text
    except:
        summary3 = None
        pass

    # recipe_data 채우기 (recipe_txt)
    try:
        recipe_data = {
            "recipe_id": recipe_id,
            "recipe_name": recipe_txt["name"],
            "author_id": author_id,
            "author_name": recipe_txt["author"]["name"],
            "ingredient": recipe_txt["recipeIngredient"],
            "time_taken": summary2,
            "difficulty": summary3,
            "portion": summary1,
            "food_img_url": recipe_txt["image"][1],
            "recipeInstructions": [
                elem["text"] for elem in recipe_txt["recipeInstructions"]
            ],
            "description": recipe_txt["description"],
            "reviewer_ids": None,
            "reviews": 0,
            "photo_reviews": 0,
            "comments": 0,
            "datePublished": recipe_txt["datePublished"],
        }
    except KeyError:
        # recipe_txt["recipeIngredient"] 없는 경우
        try:
            ingredient_elems = driver.find_elements(By.TAG_NAME, "dd")
            ingredient_lst = []
            for elem in ingredient_elems:
                if len(elem.text.split(" ")):
                    ingredient_lst.append(elem.text)

            recipe_data = {
                "recipe_id": recipe_id,
                "recipe_name": recipe_txt["name"],
                "author_id": author_id,
                "author_name": recipe_txt["author"]["name"],
                "ingredient": ingredient_lst,
                "time_taken": summary2,
                "difficulty": summary3,
                "portion": summary1,
                "food_img_url": recipe_txt["image"][1],
                "recipeInstructions": [
                    elem["text"] for elem in recipe_txt["recipeInstructions"]
                ],
                "description": recipe_txt["description"],
                "reviewer_ids": None,
                "reviews": 0,
                "photo_reviews": 0,
                "comments": 0,
                "datePublished": recipe_txt["datePublished"],
            }
        except Exception as e:
            print(recipe_id)
            print(e)
            breakpoint()
            pass

    # recipe_data 채우기 (리뷰)
    reviews_cnt = 0
    reviewer_ids = []
    try:
        reviews_cnt_elems = driver.find_elements(By.ID, "recipeCommentListCount")
        for reviews_cnt_elem in reviews_cnt_elems:
            driver.execute_script("arguments[0].scrollIntoView();", reviews_cnt_elem)
            what_text = reviews_cnt_elem.find_element(By.XPATH, "..").text.split(" ")[0]
            what_cnt = int(reviews_cnt_elem.text)

            if what_text == "요리":
                print(f"[ {recipe_id} | {what_text} | {what_cnt} ]")
                reviews_cnt = what_cnt
                recipe_data["reviews"] = reviews_cnt

                reviews_tit = reviews_cnt_elem.find_element(By.XPATH, "..")
                reviews_lst_elem = reviews_tit.find_element(
                    By.XPATH, "following-sibling::div"
                )

                reviews_divs = reviews_lst_elem.find_elements(By.XPATH, "child::div")

                for i, reviews_div in enumerate(reviews_divs):
                    driver.execute_script("arguments[0].scrollIntoView();", reviews_div)
                    if reviews_div.get_attribute("class") == "media reply_list":
                        child_div = reviews_div.find_element(By.XPATH, ".//div")
                        aTag = child_div.find_element(By.XPATH, ".//a")
                        href = aTag.get_attribute("href")
                        reviewer_id = href.split("uid=")[1]
                        reviewer_ids.append(reviewer_id)
                    elif reviews_div.get_attribute("id") == "moreViewReviewList":
                        child_review_divs = reviews_div.find_elements(
                            By.XPATH, ".//div"
                        )
                        for child_review_div in child_review_divs:
                            if (
                                child_review_div.get_attribute("class")
                                == "media reply_list"
                            ):
                                child_div2 = child_review_div.find_element(
                                    By.XPATH, ".//div"
                                )
                                aTag2 = child_div2.find_element(By.XPATH, ".//a")
                                href2 = aTag2.get_attribute("href")
                                reviewer_id2 = href2.split("uid=")[1]
                                reviewer_ids.append(reviewer_id2)

                if reviews_cnt != len(reviewer_ids):
                    print("Error-2")
                    breakpoint()

            elif what_text == "댓글":
                recipe_data["comments"] = what_cnt

            elif what_text == "포토":
                recipe_data["photo_reviews"] = what_cnt
    except:
        print(">>> Error : crawling")
        breakpoint()
        pass

    # recipe_data 채우기 (reviewer_ids)
    recipe_data["reviewer_ids"] = json.dumps(reviewer_ids)

    # recipe_url -> recipe_id 로 충분
    recipe_df = pd.DataFrame([recipe_data])

    if reviews_cnt != len(reviewer_ids):
        print(">>> Error: number of reviews")
        print(url)
        breakpoint()

    return recipe_df, reviewer_ids


def main(args):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    df = pd.read_csv(
        args.data_path + "TB_RECIPE_SEARCH-20231130.csv",
        encoding="cp949",
        low_memory=False,
        encoding_errors="ignore",
    )

    ## Test
    new_uid_lst = []
    # breakpoint()
    ### TEST
    # for recipe_id in [352110]:
    #     recipe_df, uid_lst = recipe_info(recipe_id, driver)

    #     if len(uid_lst) > 0:
    #         update_list(new_uid_lst, uid_lst)
    #         save_uid_results('user_id', new_uid_lst)
    #     save_recipe_results('recipe_data', recipe_df)

    for idx, row in df.iterrows():
        recipe_id = row["RCP_SNO"]
        recipe_df, uid_lst = recipe_info(recipe_id, driver)

        if len(uid_lst) > 0:
            update_list(new_uid_lst, uid_lst)
            save_uid_results("user_id", new_uid_lst)
        save_recipe_results("recipe_data", recipe_df)

    # print(new_uid_lst)
    breakpoint()
    save_uid_results("user_id_final", {"user_id": new_uid_lst})

    # WebDriver 종료
    driver.quit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="parser")
    arg = parser.add_argument

    arg(
        "--data_path", type=str, default="data/", help="Data path를 설정할 수 있습니다."
    )

    args = parser.parse_args()
    main(args)
