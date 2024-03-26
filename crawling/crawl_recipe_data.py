import argparse
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from tqdm import tqdm
from crawl_utils import log_exception, create_upper_folder, close_popup, save_result


class RecipeCrawler:
    def __init__(self, row):
        self.id = row["RCP_SNO"]
        self.url = f"https://www.10000recipe.com/recipe/{self.id}"
        self.row = row

    def launch_crawler(self, driver):
        self.driver = driver
        self.driver.get(self.url)
        self.driver.implicitly_wait(3)

    def crawl_recipe(self):
        recipe_data = {
            "recipe_id": self.id,
            "recipe_title": self.row["RCP_TTL"],
            "recipe_name": self.row["CKG_NM"],
            "author_id": self.row["RGTR_ID"],
            "author_name": self.row["RGTR_NM"],
            "recipe_method": self.row["CKG_MTH_ACTO_NM"],
            "recipe_status": self.row["CKG_STA_ACTO_NM"],
            "recipe_kind": self.row["CKG_KND_ACTO_NM"],
            "time_taken": self.row["CKG_TIME_NM"],
            "difficulty": self.row["CKG_DODF_NM"],
            "recipe_url": self.url,
            "portion": self.row["CKG_INBUN_NM"],
            "datePublished": self.row["FIRST_REG_DT"],
            "food_img_url": None,
            "ingredient": {},
            "reviews": 0,
            "photo_reviews": 0,
            "comments": 0,
        }

        # 사진 url
        try:
            img_elem = self.driver.find_element(By.ID, "main_thumbs")
            img_url = img_elem.get_attribute("src")
            recipe_data["food_img_url"] = img_url
        except:
            log_exception(args.log_path, str(self.id))
            pass

        # 재료
        try:
            ingredients_data = {}
            ingredient_elem = self.driver.find_element(
                By.ID, "divConfirmedMaterialArea"
            )
            ingredient_uls = ingredient_elem.find_elements(By.TAG_NAME, "ul")

            for ingredient_ul in ingredient_uls:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", ingredient_ul
                )

                b_tag = ingredient_ul.find_element(By.TAG_NAME, "b")
                b_tag_text = b_tag.text.strip("[]")

                li_tags = ingredient_ul.find_elements(By.TAG_NAME, "li")

                ingredient_data_lst = []
                for li_tag in li_tags:
                    ingredient_data = {"name": None, "amount": None}
                    ingredient_name = li_tag.find_elements(By.TAG_NAME, "a")[0].text
                    try:
                        ingredient_amount = li_tag.find_element(
                            By.CLASS_NAME, "ingre_unit"
                        ).text
                    except:
                        ingredient_amount = li_tag.find_element(
                            By.CLASS_NAME, "ingre_list_ea"
                        ).text
                    ingredient_data["name"] = ingredient_name
                    ingredient_data["amount"] = ingredient_amount

                    ingredient_data_lst.append(ingredient_data)
                ingredients_data[b_tag_text] = ingredient_data_lst
            recipe_data["ingredient"] = str(ingredients_data)
        except:
            try:
                recipe_data["ingredient"] = self.row["CKG_MTRL_CN"]
            except:
                log_exception(args.log_path, str(self.id))
                pass
            pass

        # 리뷰, 포토 리뷰, 댓글
        try:
            reviews_cnt_elems = self.driver.find_elements(By.CLASS_NAME, "view_reply")
            for reviews_cnt_elem in reviews_cnt_elems:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();", reviews_cnt_elem
                )
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
            log_exception(args.log_path, str(self.id))
            pass
        return recipe_data


def main(args):

    create_upper_folder(args.save_path)
    create_upper_folder(args.log_path)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    if args.chrome_install:
        service = ChromeService(ChromeDriverManager().install())
    else:
        service = ChromeService(executable_path=r"/usr/bin/chromedriver")

    if args.test:
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=service, options=options)

    df = pd.read_csv(args.data_path)

    for idx, row in tqdm(df.iterrows()):
        crawler = RecipeCrawler(row=row)
        recipe_data = crawler.launch_crawler(driver)
        new_recipe_data = pd.DataFrame([recipe_data])
        save_result(args.save_path, new_recipe_data)

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
        "--test",
        type=bool,
        default=False,
        help="test 여부를 설정할 수 있습니다.",
        
    )

    arg(
        "--chrome_install",
        type=bool,
        default=True,
        help="Chrome Driver Manager 로 설치 여부를 설정할 수 있습니다.",
    )

    args = parser.parse_args()
    main(args)
