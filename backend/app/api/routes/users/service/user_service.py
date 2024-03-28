import uuid
import pulp
import logging

from fastapi import HTTPException
from datetime import datetime, timedelta

from ..entity.user import User
from ..repository.user_repository import (
    UserRepository, SessionRepository, FoodRepository, RecommendationRepository, BasketRepository
)
from ..dto.user_dto import (
    UserSignupDTO, UserLoginDTO,
)
from ..controller.request.signup_request import UserFavorRecipesRequest

logging.basicConfig(level=logging.DEBUG)

class UserService:
    def __init__(self,
                 user_repository :UserRepository,
                 session_repository: SessionRepository,
                 food_repository: FoodRepository,
                 recommendation_repository: RecommendationRepository,
                 basket_repository: BasketRepository,
                 ):
        self.user_repository: UserRepository = user_repository
        self.session_repository: SessionRepository = session_repository
        self.food_repository: FoodRepository = food_repository
        self.recommendation_repository : RecommendationRepository = recommendation_repository
        self.basket_repository: BasketRepository = basket_repository

    def sign_up(self, sign_up_request: UserSignupDTO) -> UserSignupDTO:
        return self.user_repository.insert_one(sign_up_request)
    
    def login(self, login_request: UserLoginDTO):
        user = self.user_repository.find_one({'login_id': login_request.login_id, 'password': login_request.password})
        if user is None:
            raise HTTPException(status_code=400, detail="아이디와 비밀번호가 일치하지 않습니다.")

        if_first_login: bool = ('initial_feedback_history' not in user)
        user = User(**dict(user))
        
        token = str(uuid.uuid4())
        expire_date = datetime.now() + timedelta(seconds=30 * 60)

        return self.session_repository.insert_one(login_id=login_request.login_id, token=token, expire_date=expire_date), if_first_login
    
    def is_login_id_usable(self, login_id: str) -> bool:
        if self.user_repository.find_one({'login_id': login_id}) is not None:
            raise HTTPException(status_code=409, detail=f"중복되는 아이디 입니다: {login_id}")
        return True
    
    def is_nickname_usable(self, nickname: str) -> bool:
        if self.user_repository.find_one({'nickname': nickname}) is not None:
            raise HTTPException(status_code=409, detail=f"중복되는 닉네임 입니다: {nickname}")
        return True
    
    def favor_recipes(self, page_num: int) -> list:
        return self.food_repository.find_foods(page_num)
    
    def save_favor_recipes(self, login_id: str, request: UserFavorRecipesRequest) -> str:
        return self.user_repository.update_food(login_id, request.recipes)

    def top_k_recipes(self, login_id: str, price: int) -> list:
        user = self.user_repository.find_one({"login_id": login_id})
        # user에 inference된 recipes
        return self.recommendation_repository.find_by_user_id(user['_id'])
    
    def recommended_basket(self, recipe_infos: dict, price_infos: dict, price: int) -> dict:
        # 입력값 파싱
        # recipe_requirement_infos, price_infos = self._parse(recipe_infos)

        # 이진 정수 프로그래밍
        return self._optimized_results(recipe_infos, price_infos, price)
    
    def save_basket(self, user_id, price, datetime, recommended_basket, basket_price: float = 0.) -> None:
        # 추천 결과 정보 저장
        self.basket_repository.save({
            'user_id': user_id,
            'price': price,
            'datetime': datetime,
            'ingredients': recommended_basket['ingredient_list'],
            'recipes': recommended_basket['recipe_list'],
            'basket_price': recommended_basket['basket_price']})
        
        # 유저 recommend 정보 append
        self.user_repository.update_recommended_basket(user_id, recommended_basket['recipe_list'])

    def _optimized_results(self, 
                           recipe_requirement_infos: dict,
                           price_infos: dict,
                           price: int):
        # 혼합 정수 프로그래밍
        # 가격 상한
        MAX_PRICE = price

        # logging.debug("-----------[OPTIMIZING]------------")
        # logging.debug(recipe_requirement_infos)
        # logging.debug(price_infos)

        # 문제 인스턴스 생성
        prob = pulp.LpProblem("MaximizeNumberOfDishes", pulp.LpMaximize)

        # ingredients_price = {'신김치':  7000, '돼지고기': 5000, '양파': 3000, '두부': 1500, '애호박': 2000, '청양고추': 1000, '계란': 6000, '밀가루':  3000}
        # 식재료 가격 및 판매단위 변수 (0 또는 1의 값을 가짐)
        ingredient_use_variable = pulp.LpVariable.dicts("ingredient", price_infos.keys(), cat='Binary') # 재료 포함 여부

        # 요리 변수
        # dishes = ['Dish1', 'Dish2']
        dishes = recipe_requirement_infos.keys()
        # dishes = ['돼지고기김치찌개', '된장찌개', '애호박전']
        dish_use_variable = pulp.LpVariable.dicts("dish", dishes, cat='Binary') # 요리 포함 여부

        # 요리별 필요한 식재료 양
        # requirements = {'Dish1': {'A': 5, 'B': 2}, 'Dish2': {'B': 2, 'C': 2}}
        # requirements = {'돼지고기김치찌개': ['신김치', '돼지고기', '양파', '두부'], '된장찌개': ['두부', '애호박', '청양고추', '양파'], '애호박전': ['애호박', '계란', '밀가루']}

        # 식재료 제한: 각 요리를 최대한 살 수 있는 한도
        # a = {ingredient: (MAX_PRICE//info['price'])*info['amount'] \
        #                                     for ingredient, info in price_infos.items()}
        # print(a)

        # 목표 함수 (최대화하고자 하는 요리의 수)
        prob += pulp.lpSum([dish_use_variable[dish] for dish in dishes])

        # 비용 제약 조건
        prob += pulp.lpSum([price_infos[i]['price']*ingredient_use_variable[i] for i in price_infos]) <= MAX_PRICE

        # 요리별 식재료 제약 조건
        for dish in dishes:
            for ingredient in recipe_requirement_infos[dish]:
                prob += (ingredient_use_variable[ingredient] >= dish_use_variable[dish])

        # 정량 제약 조건: 요리에 사용되는 재료의 총합은 각 재료의 상한을 넘지 못함
        # for ingredient in price_infos.keys():
        #     total_amount = pulp.lpSum([y[dish] * requirement[ingredient] for dish, requirement in recipe_requirement_infos.items() if ingredient in requirement])
        #     prob += (total_amount <= a[ingredient] * x[ingredient])

        # 문제 풀기
        prob.solve()

        # 결과 출력
        # print("Status:", pulp.LpStatus[prob.status])

        for dish in dishes:
            print(f"Make {dish}:", dish_use_variable[dish].varValue)
        for ingredient in price_infos:
            print(f"Use Ingredient {ingredient}:", ingredient_use_variable[ingredient].varValue)
        result_dish = [dish for dish in dishes if dish_use_variable[dish].varValue == 1]
        result_ingredient = [ingredient for ingredient in price_infos if ingredient_use_variable[ingredient].varValue == 1]

        return {'recipe_list' : result_dish, 'ingredient_list': result_ingredient}
