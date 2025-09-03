from pydantic import BaseModel

class Food(BaseModel):
    name: str
    description: str
    address: str
    location: str
    price_min: float
    price_max: float
    review_score_on_5: float

class FoodList(BaseModel):
    foods: list[Food]