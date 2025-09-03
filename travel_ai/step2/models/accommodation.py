from pydantic import BaseModel

class Accommodation(BaseModel):
    name: str
    description: str
    location: str
    price_min: float
    price_max: float
    review_score_on_5: float

class AccommodationList(BaseModel):
    accommodations: list[Accommodation]