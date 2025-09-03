from pydantic import BaseModel

class Accommodation(BaseModel):
    name: str
    description: str
    location: str
    local_currency_price_min: float
    local_currency_price_max: float
    euro_currency_price_min: float
    euro_currency_price_max: float
    review_score_on_5: float

class AccommodationList(BaseModel):
    accommodations: list[Accommodation]