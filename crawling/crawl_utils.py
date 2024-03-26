import os, re
import pandas as pd
from selenium.webdriver.common.by import By


def log_exception(fname, log):
    with open(fname, "a+") as log_file:
        log_file.write(log + "\n")


def create_upper_folder(fpath):
    folder_path = os.path.dirname(fpath)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"폴더 '{folder_path}' 생성")


def iso_format_time(current_time):
    return current_time.strftime("%Y-%m-%dT%H:%M")


def price2num(price_text):
    pattern = re.compile(r"\d+")
    numbers = pattern.findall(price_text)
    price = "".join(numbers)
    return int(price)


def close_popup(driver):
    try:
        close_btn = driver.find_element(By.XPATH, "//*[@id='popup_goods']/a")
        close_btn.click()
    except Exception as e:
        pass


def save_result(fpath, data):

    df = pd.DataFrame(data)
    if os.path.exists(fpath):
        df.to_csv(fpath, mode="a", index=False, header=False)
    else:
        df.to_csv(fpath, index=False)
