from pydantic import BaseModel


class RecipeStatusUpadateRequest(BaseModel):
    feedback: bool