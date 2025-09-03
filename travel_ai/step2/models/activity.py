from pydantic import BaseModel

class Activity(BaseModel):
    name: str
    description: str
    duration: int
    location: str
    price_min: float
    price_max: float
    review_score_on_5: float

class ActivityList(BaseModel):
    activities: list[Activity]