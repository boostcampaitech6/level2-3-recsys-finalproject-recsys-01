import uvicorn
from fastapi import FastAPI, APIRouter
from api.routes.users.controller.user_controller import user_router
from api.routes.recipes.controller.recipes_controller import recipes_router

def new_app() -> FastAPI:
    return FastAPI()

app = new_app()

router = APIRouter()

@router.get('/')
def hello():
    return 'hello'

app.include_router(router)
app.include_router(user_router)
app.include_router(recipes_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
