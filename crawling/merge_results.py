import os
from datetime import datetime as dt

import numpy as np
import pandas as pd

def main():
    today = dt.now().strftime('%y%m%d')
    all_files = os.listdir('usercrawlresult')
    
    recipes, reviews = [], []

    for filename in all_files:
        if filename.startswith('recipes'):
            recipes.append(pd.read_csv('usercrawlresult/'+filename))
        elif filename.startswith('reviews'):
            reviews.append(pd.read_csv('usercrawlresult/'+filename))

    print(f'num of recipes files: {len(recipes)}')
    print(f'num of reviews files: {len(reviews)}')

    recipes = pd.concat(recipes, axis=0)
    reviews = pd.concat(reviews, axis=0)

    recipes.to_csv(f'usercrawlresult/recipes_full_{today}.csv', index=False)
    reviews.to_csv(f'usercrawlresult/reviews_full_{today}.csv', index=False)

if __name__ == '__main__':
    main()
