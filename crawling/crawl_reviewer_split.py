import numpy as np
import pandas as pd 


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

def read_crawled_df(filename):
    return pd.read_csv(filename)

def main():
    # get all recipe snos
    recipe_snos = get_recipesno_set()

    crawled_dfs = []
    for filename in ['reviewers_240302.csv', 'reviewers_240303.csv', 'reviewers_240304.csv']:
        crawled_dfs.append(read_crawled_df(filename))

    crawled_df = pd.concat(crawled_dfs, axis=0)
    crawled_recipe_snos = set(crawled_df.recipe_sno.values)

    target_recipe_snos = recipe_snos - crawled_recipe_snos
    print(len(recipe_snos))
    print(len(crawled_recipe_snos))
    print(len(target_recipe_snos))
    divided_snos = np.array_split(np.array(list(target_recipe_snos)), 4)

    for i, divided_sno in enumerate(divided_snos):
        np.save(f'recipe_sno_{i}.npy', divided_sno)

if __name__ == '__main__':
    main()
