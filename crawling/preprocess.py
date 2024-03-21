import time, sys
import multiprocessing
import concurrent.futures
import pandas as pd

from datetime import datetime as dt
from pydantic import BaseModel
from pymongo.collection import Collection
from openai import OpenAI
from tqdm import tqdm

from database.data_source import data_source
from database.data_source import data_source

class Recipe(BaseModel):
    recipe_id: str
    recipe_title: str
    recipe_name: str 
    author_id: str
    author_name: str
    recipe_method: str
    recipe_status: str
    recipe_kind: str
    time_taken: str
    difficulty: str
    recipe_url: str
    date_published: str
    img_url: str
    ingredients: str
    review_count: int
    photo_review_count: int
    comment_count: int
    portion: str

class Preprocess:
    MAIN_CATEGORIES = set([
        '주재료',
        '재료',
    ])

    def __init__(self, data_file: str, api_key: str='AZC391KuQY9F1kWzQQntTU7fUoqffp4e'):
        self.data: pd.DataFrame = self._na_replaced(pd.read_csv(data_file))
        self.recipe_repository: Collection = data_source.collection_with_name_as('recipes')
        self.ingredient_repository: Collection = data_source.collection_with_name_as('ingredients')
        self.llm_client: OpenAI = OpenAI(
            api_key=api_key,
            base_url="https://api.upstage.ai/v1/solar"
        )
        self.run_time = dt.strftime(dt.now(), '%Y%m%d%H%M%S')

    def _na_replaced(self, df: pd.DataFrame):
        '''
        recipe_id         int64 recipe_id            0
        recipe_title     object recipe_title        44
        recipe_name      object recipe_name        119
        author_id        object author_id           44
        author_name      object author_name       1618
        recipe_method    object recipe_method     4505
        recipe_status    object recipe_status     5544
        recipe_kind      object recipe_kind       4505
        time_taken       object time_taken       18521
        difficulty       object difficulty        2390
        recipe_url       object recipe_url           0
        portion          object portion           6911
        datePublished    object datePublished       53
        food_img_url     object food_img_url       266
        ingredient       object ingredient           0
        reviews           int64 reviews              0
        photo_reviews     int64 photo_reviews        0
        comments          int64 comments             0
        '''
        default_value = {
            'recipe_id': '9' * 7,
            'recipe_title': '맛있는 요리',
            'recipe_name': '맛있는 요리',
            'author_id': '9' * 7,
            'author_name': '작자미상',
            'recipe_method': '모름',
            'recipe_status': '모름',
            'recipe_kind': '모름',
            'time_taken': '모름',
            'difficulty': '초급',
            'recipe_url': 'https://www.10000recipe.com/index.html',
            'portion' : '1인분',
            'datePublished': dt.strftime(dt.now(), '%y%m%d%H%M%S'),
            'food_img_url': 'https://media.istockphoto.com/id/1283988510/ko/%EB%B2%A1%ED%84%B0/%EC%9D%BC%EB%B3%B8%EC%8B%9D-%EB%B0%A5.jpg?s=612x612&w=0&k=20&c=wr2rxOgUQbpaPBEC6PHqjS7B2b5_WQGcs5ujZERhX3U=',
            'ingredient': "{'주재료': {'name': '밥', 'amount': '1공기'}}",
            'reviews': 0,
            'photo_reviews': 0,
            'comments': 0
        }
        df.fillna(default_value, inplace=True)
        return df
    
    def multi_thread_run(self):
        # with multiprocessing.Pool(processes=8) as pool:

        # # with tqdm(total=len(self.data)) as pbar:
        # #     for result in pool.map(self.run, self.data):
        # #         pbar.update()
        #     result = pool.imap(self.run, self.data)
        #     print(result.next())

        # pool.close()
        # pool.join()

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     tqdm(executor.map(self.run, self.data), total=len(self.data))
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            num_groups = 8
            group_size = len(self.data) // num_groups
            grouped_dfs = [self.data.iloc[i*group_size:(i+1)*group_size] for i in range(num_groups)]

            # 각 항목을 멀티 스레드로 처리하고 결과를 수집
            futures = [executor.submit(self.run, df) for df in grouped_dfs]
            
            # tqdm을 사용하여 진행 상황 모니터링
            with tqdm(total=len(self.data)) as pbar:
                for future in concurrent.futures.as_completed(futures):
                    # 결과를 얻어와서 처리
                    result = future.result()
                    # tqdm을 사용하여 진행 상황 업데이트
                    pbar.update()

    def multi_processing_run(self):
        with multiprocessing.Pool(processes=8) as pool:
            result = pool.imap(self.run, self.data)
            

    def run(self, data):
        # 1. 데이터 로드
        # 2.1. recipe 단위 인스턴스 생성
            # 'recipe_id', 'recipe_title', 'recipe_name', 'author_id', 'author_name',
            #    'recipe_method', 'recipe_status', 'recipe_kind', 'time_taken',
            #    'difficulty', 'recipe_url', 'portion', 'datePublished', 'food_img_url',
            #    'ingredient', 'reviews', 'photo_reviews', 'comments'
        
        ingredients_count = 0

        for idx, row in tqdm(data.iterrows(), total = data.shape[0]):
            if self.recipe_repository.find_one({'recipe_name': row['recipe_title']}):
                continue

            try:
                recipe: Recipe = Recipe(
                    recipe_id=str(row['recipe_id']),
                    recipe_title=row['recipe_title'],
                    recipe_name=row['recipe_name'],
                    author_id=str(row['author_id']),
                    author_name=row['author_name'],
                    recipe_method=row['recipe_method'],
                    recipe_status=row['recipe_status'],
                    recipe_kind=row['recipe_kind'],
                    time_taken=row['time_taken'],
                    difficulty=row['difficulty'],
                    recipe_url=row['recipe_url'],
                    portion=row['portion'],
                    date_published=str(row['datePublished']),
                    img_url=row['food_img_url'],
                    ingredients=row['ingredient'],
                    review_count=row['reviews'],
                    photo_review_count=row['photo_reviews'],
                    comment_count=row['comments']   
                )
                
                # 2.2. ingredients name 추출
                recipe.ingredients = Preprocess.dict_ingredients(recipe.ingredients) # dict로 변경
                # print('Dict', recipe.ingredients)

                # 2.2.1. 주재료 필터링
                recipe.ingredients = Preprocess.main_filtered(recipe.ingredients)
                # print('Filter', recipe.ingredients)

                # 3. ingredients 저장 및 id 리스트 반환
                recipe.ingredients = self.inserted_ingredient_documents(recipe.ingredients)
                # print('ID', recipe.ingredients)
                
                ingredients_count += len(recipe.ingredients) # name 업데이트 위함

                # 4. recipes 저장
                self.insert_recipe(recipe)

            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                pass
        
        self.ingredients_count = ingredients_count

    
    def rename_ingredient_names(self, batch_size: int=500) -> int:
        # batch_size개 ingredients 조회
        skip = 0
        total_iter_count = self.ingredients_count // batch_size + 1
        modified_count = 0

        for _ in tqdm(range(total_iter_count)):
            # batch_size개씩 문서를 조회하여 가져옴
            batch_ingredients = self.recipe_repository.find({}, {'name':1}).skip(skip).limit(batch_size)

            # name만 반환
            ingredient_names = [ingredient['name'] for ingredient in batch_ingredients]

            # ingredients name solar 변환
            ingredient_names = self.llm_parsed_ingredients(ingredient_names)
            
            # name 내 space 제거
            ingredient_names = Preprocess.without_space(ingredient_names)

            # 기존 이름 업데이트
            for name in ingredient_names:
                for old_name, new_name in name.items():
                    result = self.ingredient_repository.update_many({'name': old_name}, {'$set': {'name': new_name}})
                    modified_count += result.modified_count
    
            # 다음 조회를 위해 skip 값을 업데이트
            skip += batch_size
        
        return modified_count
    

    @staticmethod
    def without_space(ingredients: list[dict]):
        for ingredient in ingredients:
            ingredient['name'] = ingredient['name'].replace(' ', '')
        return ingredients

    @staticmethod
    def dict_ingredients(ingredient: str) -> dict:
        try:
            return eval(ingredient)
        except:
            return {}
        
    @staticmethod
    def main_filtered(info: dict) -> list[dict]:
        ret = list()
        # ingredient={
        #   '재료': [{'name': '또띠아', 'amount': '1장'}, {'name': '모짜렐라치즈', 'amount': '마음껏'}, {'name': '꿀', 'amount': '마음껏'}, {'name': '다진마늘', 'amount': '1스푼'}, {'name': '버터', 'amount': '1스푼'}]
        # }
        for category, ingredients in info.items():
            if category in Preprocess.MAIN_CATEGORIES: # 메인 카테고리에 포함되면 계속 추가
                for ingredient in ingredients:
                    ret.append(ingredient)
                continue
            if len(ret) == 0: # 메인 카테고리에 해당하는 대상이 없으면 첫번째 카테고리만 포함시킴
                for ingredient in ingredients:
                    ret.append(ingredient)
                break
        return ret
    
    def _names_of(ingredients: list[dict]) -> list[str]:
        return [ingredient['name'] for ingredient in ingredients]
    
    def _llm_stream(self, ingredient_names: list[str]):
        try:
            return self.llm_client.chat.completions.create(
                model="solar-1-mini-chat",
                messages=[
                    {
                    "role": "system",
                    "content": "사용자가 한국 이커머스 사이트에서 식재료를 검색하여 구매하려고 해. 사용자가 입력하는 식재료명은 직접 검색어로 입력하였을 때에 식재료와 잘 매칭되지 않을 수 있어서, 검색이 가능한 형태로 변형하고 싶어. 검색 가능한 키워드로 바꿔주는 파이썬 딕셔너리를 반환해줘. 딕셔너리의 형태는 {<기존식재료명1>: <변형할 식재료명1>, <기존식재료명2>: <변형할 식재료명2>, ...} 으로 부탁해. 식재료명은 모두 한국어로 해주고, 변형이 어려운 식재료의 경우 변형할 식재료 명을 None으로 입력해도 좋아"
                    },
                    {
                    "role": "user",
                    "content": f"{ingredient_names}"
                    }
                ],
                stream=True,
                temperature=0.2,
            )
        except:
            return None
    
    def llm_parsed_ingredients(self, ingredients: list[dict]) -> list[dict]:
        # 재료의 이름 모음
        ingredient_names = Preprocess._names_of(ingredients)

        # solar stream 생성
        stream = Preprocess._llm_stream(ingredient_names)

        retry_count = 0
        while stream is None:
            if retry_count == 10:
                raise ValueError('재시도 횟수 초과')
            time.sleep(2)
            stream = Preprocess._llm_stream(ingredient_names)
            print(f"재시도 {retry_count}")
            retry_count += 1

        # 결과 파싱
        llm_dict = Preprocess._parsed_llm_output(stream)
        
        # dict 형태로 변환: 에러시 오류..
        try:
            llm_dict = eval(llm_dict)
        except:
            with open(f'llm_output/error_.txt', 'a') as file:
                file.write(str({
                    'input': ingredients,
                    'output': llm_dict
                }))
        
        # 생성된 매핑 딕셔너리로 기존 dict name replace
        replaced_ingredients = Preprocess._replaced_name_ingredients(ingredients, llm_dict)

        return replaced_ingredients
    
    @staticmethod
    def _replaced_name_ingredients(ingredients: list[dict], llm_dict: dict):
        for ingredient in ingredients:
            if ingredient['name'] not in llm_dict: # 이름이 존재하지 않으면 그냥 넘김
                continue

            replaced_name = llm_dict[ingredient['name']]
            if replaced_name is None: # 결과가 None 이면 그냥 넘김
                continue

            ingredient['name'] = replaced_name

        return ingredients
    
    @staticmethod
    def _parsed_llm_output(stream) -> str:
        output = []
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                # print(content, end="")
                output.append(content)

        # print("\n-----------")
        output = "".join(output)
        # print(output)
        start_idx, end_idx = output.find('{'), output.find('}')
        output = output[start_idx:end_idx+1]

        with open(f'llm_output/_.txt', 'a') as file:
            file.write(output)
        
        return output
    
    @staticmethod
    def split_value_and_unit(input_string):
        idx = -1
        reversed_string = input_string[::-1]
        for i, c in enumerate(reversed_string):
            if c.isdigit():
                idx = i
                break

        idx = len(input_string)-idx
        value = input_string[:idx]
        unit = input_string[idx:]

        return value if (len(value) > 0) else '1', unit if (len(unit) > 0) else '개'
    
    def inserted_ingredient_documents(self, ingredient_names: list[dict]) -> list[str]:
        ingredient_ids = list()
        for ingredient_name in ingredient_names:
            ingredient_ids.append(self._ingredient_id(ingredient_name))
        # ingredients id 리스트로 변환
        return ingredient_ids
    
    def _ingredient_id(self, ingredient: dict) -> str:
        # ingredients collection search by name
        # print(ingredient)
        id = self.ingredient_repository.find_one({
            'name': ingredient['name']
        })
        if id:
            return str(id['_id'])
        
        # ingredients collection insert
        return str(
            self.ingredient_repository.insert_one({
            'name': ingredient['name'],
            'amount': Preprocess._parsed_amount(ingredient['amount'])
        }).inserted_id)
    
    @staticmethod
    def _parsed_amount(amount: str) -> dict:
        if amount is None:
            return {
                'value': '1',
                'unit': '개'
            }
        
        value, unit = Preprocess.split_value_and_unit(amount.strip())
        return {
            'value': value,
            'unit': unit
        }
    
    def insert_recipe(self, recipe: Recipe) -> None:
        self.recipe_repository.insert_one({
            'food_name': recipe.recipe_name,
            'recipe_name': recipe.recipe_title,
            'ingredients': recipe.ingredients,
            'time_taken': recipe.time_taken,
            'difficulty': recipe.difficulty,
            'recipe_url': recipe.recipe_url,
            'portion': recipe.portion,
            'recipe_img_url': recipe.img_url,
        })
        

if __name__ == '__main__':

    count = sys.argv[-1]

    preprocess = Preprocess(f'recipe_data_merged_{count}.csv')

    preprocess.run()