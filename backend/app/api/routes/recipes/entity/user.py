from pydantic import BaseModel, Field, ConfigDict
from typing import List
from .....utils.pyobject_id import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(alias='_id', default=None)
    user_nickname: str
    user_name: str
    user_email: str
    user_password: str
    allergy: List[PyObjectId] = []
    recommend_history_by_model: List[PyObjectId] = []
    recommend_history_by_basket: List[PyObjectId] = []
    feedback_history: List[PyObjectId] = []
    initial_feedback_history: List[PyObjectId] = []
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "user_id",
                "user_nickname": "johndoe",
                "user_name": "John Doe",
                "user_email": "john.doe@example.com",
                "user_password": "secret_password",
                "allergy": [],
                "recommend_history_by_model": [],
                "recommend_history_by_basket": [],
                "feedback_history": [],
                "initial_feedback_history": [],
            }
        },
    )

    
    def get_feedback_history(self) -> List[str]:
        return self.feedback_history
    
    def get_recommend_history_by_basket(self) -> List[str]:
        return self.recommend_history_by_basket