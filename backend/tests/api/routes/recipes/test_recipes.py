import pytest
from .....app.api.routes.recipes.repository.recipes_repository import select_user_by_user_id, select_recipes_by_recipes_id, select_ingredients_by_ingredients_id
from.....app.api.routes.recipes.entity.user import User
from.....app.api.routes.recipes.entity.recipes import Recipes
from.....app.api.routes.recipes.entity.recipe import Recipe

from fastapi.testclient import TestClient
from .....app.api.routes.recipes.controller.recipes_controller import recipes_router


# User Type 확인
@pytest.mark.parametrize("user_id, output", [
    ('65f0063d141b7b6fd385c7cc', True),
])
def test_select_user_by_user_id_type(user_id, output):
    user = select_user_by_user_id(user_id)
    assert isinstance(user, User) == output
    

# user_id로 유저룰 알맞게 가져 오는지 테스트
@pytest.mark.parametrize("user_id, output", [
    ('65f0063d141b7b6fd385c7cc',
     {
        "id": "65f0063d141b7b6fd385c7cc",
        "user_nickname": "Son",
        "user_name": "손흥민",
        "user_email": "aaa@naver.com",
        "user_password": "0000",
        "allergy": [
            "65f01320141b7b6fd385c7d4",
            "65f01320141b7b6fd385c7d4"
        ],
        "recommend_history_by_model": [
            "65f01320141b7b6fd385c7d4",
            "65f01320141b7b6fd385c7d4"
        ],
        "recommend_history_by_basket": [
            "65f01320141b7b6fd385c7d4",
            "65f01320141b7b6fd385c7d4"
        ],
        "feedback_history": [
            "65f0371e141b7b6fd385c7d8",
            "65f29506141b7b6fd385c7e9"
        ],
        "initial_feedback_history": [
            "65f01320141b7b6fd385c7d4",
            "65f01320141b7b6fd385c7d4"
        ]
    }
     ),
])
def test_select_user_by_user_id(user_id, output):
    user = select_user_by_user_id(user_id)
    assert user.model_dump() == output


# feedback list로 레시피를 올바르게 조회하는지 테스트 
@pytest.mark.parametrize("recipes_id, output", [
    (["65f0371e141b7b6fd385c7d8", "65f0371e141b7b6fd385c7d8"], True),
])
def test_select_recipes_by_recipes_id(recipes_id, output):
    recipes = select_recipes_by_recipes_id(recipes_id)
    assert isinstance(recipes, Recipes) == output
    assert isinstance(recipes.get_recipes()[0], Recipe) == output
    
    
# 레시피에서 재료 올바르게 조회하는지 테스트
@pytest.mark.parametrize("ingredients_id, output", [
    (["65f04741141b7b6fd385c7da", "65f047b9141b7b6fd385c7db"], []),
])
def test_select_ingredients_by_ingredients_id(ingredients_id, output):
    recipes = select_ingredients_by_ingredients_id(ingredients_id)
    
    
# API 테스트
client = TestClient(recipes_router)

@pytest.mark.parametrize("user_id, output", [
    ("65f0063d141b7b6fd385c7cc", 
     {
  "response": [
    {
      "id": "65f0371e141b7b6fd385c7d8",
      "recipe_name": "매콤한 김치찌개",
      "ingredient": {
        "65f04741141b7b6fd385c7da": "김치",
        "65f047b9141b7b6fd385c7db": "삼겹살"
      },
      "recipe_url": "https://www.10000recipe.com/recipe/view.html?seq=6908832&targetList=reviewLists#reviewLists",
      "recipe_img_url": "https://recipe1.ezmember.co.kr/cache/recipe/2019/03/10/ad0e61fd8b4783a926ebccadd0c1b8c11.jpg"
    },
    {
      "id": "65f29506141b7b6fd385c7e9",
      "recipe_name": "맛있는 제육볶음",
      "ingredient": {
        "65f29547141b7b6fd385c7eb": "고추장",
        "65f2955e141b7b6fd385c7f1": "양파"
      },
      "recipe_url": "https://www.10000recipe.com/recipe/view.html?seq=6908832&targetList=reviewLists#reviewLists",
      "recipe_img_url": "https://recipe1.ezmember.co.kr/cache/recipe/2019/03/10/ad0e61fd8b4783a926ebccadd0c1b8c11.jpg"
    }
  ]
}
     ),
])
def test_read_item(user_id, output):
    response = client.get(f"/users/{user_id}/recipes/cooked")
    assert response.status_code == 200
    assert response.json() == output

