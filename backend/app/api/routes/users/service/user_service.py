import uuid
import pulp

from datetime import datetime, timedelta

from ..entity.user import User
from ..repository.user_repository import UserRepository, SessionRepository, FoodRepository, RecommendationRepository
from ..dto.user_dto import (
    UserSignupDTO, UserLoginDTO,
)
from ..controller.request.signup_request import UserFavorRecipesRequest

class UserService:
    def __init__(self,
                 user_repository :UserRepository,
                 session_repository: SessionRepository,
                 food_repository: FoodRepository,
                 recommendation_repository: RecommendationRepository,
                 ):
        self.user_repository: UserRepository = user_repository
        self.session_repository: SessionRepository = session_repository
        self.food_repository: FoodRepository = food_repository
        self.recommendation_repository : RecommendationRepository = recommendation_repository

    def sign_up(self, sign_up_request: UserSignupDTO) -> UserSignupDTO:
        return self.user_repository.insert_one(sign_up_request)
    
    def login(self, login_request: UserLoginDTO) -> UserLoginDTO:
        user = self.user_repository.find_one({'login_id': login_request.login_id, 'password': login_request.password})
        if user is None:
            raise ValueError("아이디와 비밀번호가 일치하지 않습니다.")
        user = User(**dict(user))
        
        token = str(uuid.uuid4())
        expire_date = datetime.now() + timedelta(seconds=30 * 60)
        return self.session_repository.insert_one(login_id=login_request.login_id, token=token, expire_date=expire_date)
    
    def is_login_id_usable(self, login_id: str) -> bool:
        if self.user_repository.find_one({'login_id': login_id}) is not None:
            raise ValueError(f"중복되는 아이디 입니다: {login_id}")
        return True
    
    def is_nickname_usable(self, nickname: str) -> bool:
        if self.user_repository.find_one({'nickname': nickname}) is not None:
            raise ValueError(f"중복되는 닉네임 입니다: {nickname}")
        return True
    
    def favor_recipes(self, page_num: int) -> list:
        return self.food_repository.find_foods(page_num)
    
    def save_favor_recipes(self, login_id: str, request: UserFavorRecipesRequest) -> None:
        self.user_repository.update_food(login_id, request.recipes)

    def top_k_recipes(self, login_id: str, price: int) -> list:
        # user에 inference된 recipes
        return self.recommendation_repository.find({'login_id': login_id})
    
    def recommended_basket(self, recipe_infos: dict, price: int) -> dict:
        # 입력값 파싱
        recipe_requirement_infos, price_infos = self._parse(recipe_infos)

        # 이진 정수 프로그래밍
        return self._optimized_results(recipe_requirement_infos, price_infos, price)

    def _parse(self, recipe_infos: dict):
        recipe_requirement_infos, price_infos = None, None
        return recipe_requirement_infos, price_infos

    def _optimized_results(self, 
                           recipe_requirement_infos: dict,
                           price_infos: dict,
                           price: int):
        # 혼합 정수 프로그래밍
        # 가격 상한
        MAX_PRICE = price

        # 문제 인스턴스 생성
        prob = pulp.LpProblem("MaximizeNumberOfDishes", pulp.LpMaximize)

        # ingredients_info = {
        #     'A': {'price': 70, 'amount': 5},
        #     'B': {'price': 30, 'amount': 2},
        #     'C': {'price': 20, 'amount': 2}}
        # ingredients_price = {'신김치':  7000, '돼지고기': 5000, '양파': 3000, '두부': 1500, '애호박': 2000, '청양고추': 1000, '계란': 6000, '밀가루':  3000}
        # 식재료 가격 및 판매단위 변수 (0 또는 1의 값을 가짐)
        x = pulp.LpVariable.dicts("ingredient", price_infos.keys(), cat='Binary') # 재료 포함 여부

        # 요리 변수
        # dishes = ['Dish1', 'Dish2']
        dishes = recipe_requirement_infos.keys()
        # dishes = ['돼지고기김치찌개', '된장찌개', '애호박전']
        y = pulp.LpVariable.dicts("dish", dishes, cat='Binary') # 요리 포함 여부

        # 요리별 필요한 식재료 양
        # requirements = {'Dish1': {'A': 5, 'B': 2}, 'Dish2': {'B': 2, 'C': 2}}
        # requirements = {'돼지고기김치찌개': ['신김치', '돼지고기', '양파', '두부'], '된장찌개': ['두부', '애호박', '청양고추', '양파'], '애호박전': ['애호박', '계란', '밀가루']}

        # 식재료 제한: 각 요리를 최대한 살 수 있는 한도
        a = {ingredient: (MAX_PRICE//info['price'])*info['amount'] \
                                            for ingredient, info in price_infos.items()}
        print(a)

        # 목표 함수 (최대화하고자 하는 요리의 수)
        prob += pulp.lpSum([y[dish] for dish in dishes])

        # 비용 제약 조건
        prob += pulp.lpSum([price_infos[i]['price']*x[i] for i in price_infos]) <= MAX_PRICE

        # 요리별 식재료 제약 조건
        for dish in dishes:
            for ingredient in recipe_requirement_infos[dish].keys():
                prob += (x[ingredient] >= y[dish])

        # 정량 제약 조건: 요리에 사용되는 재료의 총합은 각 재료의 상한을 넘지 못함
        for ingredient in price_infos.keys():
            total_amount = pulp.lpSum([y[dish] * requirement[ingredient] for dish, requirement in recipe_requirement_infos.items() if ingredient in requirement])
            prob += (total_amount <= a[ingredient] * x[ingredient])

        # 문제 풀기
        prob.solve()

        # 결과 출력
        print("Status:", pulp.LpStatus[prob.status])
        
        for dish in dishes:
            print(f"Make {dish}:", y[dish].varValue)
        for ingredient in price_infos:
            print(f"Use Ingredient {ingredient}:", x[ingredient].varValue)
        result_dish = [dish for dish in dishes if y[dish].varValue == 1]
        result_ingredient = [ingredient for ingredient in price_infos if x[ingredient].varValue == 1]

        return {'recipe_list' : result_dish, 'ingredient_list': result_ingredient}