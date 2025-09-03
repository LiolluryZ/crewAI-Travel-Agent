from pydantic import BaseModel

class City(BaseModel):
    name: str
    best_transport_to_come: str


class Transport(BaseModel):
    type: str
    from_city: str
    to_city: str
    euro_price_min: float
    euro_price_max: float
    average_duration_in_hours: float

class MacroPlanning(BaseModel):
    ordered_cities: list[City] = []
    travel_considerations: list[str] = []
    local_currency: str = ""
    current_exchange_rate: float = 0.0
    transports: list[Transport] = []