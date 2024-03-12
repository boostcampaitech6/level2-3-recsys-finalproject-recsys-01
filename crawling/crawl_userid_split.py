import numpy as np
import pandas as pd 


def get_userid_from_recipe_reviews():

    # filenames
    crawled_files = [
        'reviewers_240302.csv', 'reviewers_240303.csv', 
        'reviewers_240304.csv', 'reviewers_240305.csv', 
    ]

    df = pd.concat([pd.read_csv('data/'+f) for f in crawled_files], axis=0)
    unique_users = set(np.concatenate(df['reviewers'].apply(eval).values))
    
    return unique_users

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
    # get all user_ids
    user_ids = get_userid_from_recipe_reviews()
    divided_userids = np.array_split(np.array(list(user_ids)), 4)

    for i, divided_userid in enumerate(divided_userids):
        np.save(f'userid_from_recipe_reviews_{i}.npy', divided_userid)

if __name__ == '__main__':
    main()
