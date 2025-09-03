from pydantic import BaseModel

class City(BaseModel):
    name: str
    transport_to_come: str
    transport_price_min: float
    transport_price_max: float


class MacroPlanning(BaseModel):
    ordered_cities: list[City] = []
    travel_considerations: list[str] = []
    local_currency: str = ""
    current_exchange_rate: float = 0.0