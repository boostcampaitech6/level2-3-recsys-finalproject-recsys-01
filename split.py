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


def main(args):

    if not os.path.exists(args.split_path):
        os.makedirs(args.split_path)
        print(f">>>> 폴더 생성: {args.split_path}")
    else:
        print(f">>>> 폴더 있음: {args.split_path}")
    
    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)
        print(f">>>> 폴더 생성: {args.save_path}")
    else:
        print(f">>>> 폴더 있음: {args.save_path}")

    df = pd.read_csv(
        args.data_path + "TB_RECIPE_SEARCH-20231130.csv",
        encoding="cp949",
        low_memory=False,
        encoding_errors="ignore",
    )

    total_rows = len(df)
    for i in range(0, total_rows, 10000):
        new_df = df.iloc[i : i + 10000]
        new_df.to_csv(
            args.split_path + f"TB_RECIPE_SEARCH-20231130_{i//10000}.csv", index=False
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="parser")
    arg = parser.add_argument

    arg(
        "--data_path",
        type=str,
        default="data/",
        help="Data path를 설정할 수 있습니다.",
    )

    arg(
        "--split_path",
        type=str,
        default="data/split/",
        help="Data path를 설정할 수 있습니다.",
    )
    
    arg(
        "--save_path",
        type=str,
        default="save/split/",
        help="Data path를 설정할 수 있습니다.",
    )

    args = parser.parse_args()
    main(args)
