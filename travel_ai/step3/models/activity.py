from pydantic import BaseModel

class Activity(BaseModel):
    name: str
    description: str
    duration: int
    location: str
    local_currency_price_min: float
    local_currency_price_max: float
    euro_currency_price_min: float
    euro_currency_price_max: float
    review_score_on_5: float

class ActivityList(BaseModel):
    activities: list[Activity]