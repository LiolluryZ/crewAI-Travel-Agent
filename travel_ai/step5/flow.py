
from crewai.flow.flow import Flow, listen, start, router, or_
from pydantic import BaseModel, Field

from travel_ai.step5.crew_accommodation import AccommodationCrew
from travel_ai.step5.crew_activity import ActivityCrew
from travel_ai.step5.crew_border import BorderCrew
from travel_ai.step5.crew_food import FoodCrew
from travel_ai.step5.crew_macro import MacroCrew
from travel_ai.step5.models.accommodation import Accommodation
from travel_ai.step5.models.activity import Activity
from travel_ai.step5.models.check_border import CheckBorder
from travel_ai.step5.models.food import Food
from travel_ai.step5.models.macro_planning import MacroPlanning


class TravelState(BaseModel):
    original_country: str = Field("", description="Original country")
    destination_country: str = Field("", description="Destination country")
    date: str = Field("", description="Travel date")
    traveler_count: int = Field(0, description="Number of travelers")
    cities_queue: list[str] = Field([], description="Technical list of cities")

    macro_planning: MacroPlanning = Field(None, description="Macro planning details")
    activities: list[Activity] = Field([], description="Activities planned for each city")
    foods: list[Food] = Field([], description="Foods planned for each city")
    accommodations: list[Accommodation] = Field([], description="Accommodations planned for each city")
    borders: list[CheckBorder] = Field([], description="Border check details")

class TravelFlow(Flow[TravelState]):
    @start()
    def initialize(self):
        self.state.original_country = "France"
        self.state.destination_country = "Vietnam"
        self.state.date = "mars 2026"
        self.state.traveler_count = 2

        macro_crew = MacroCrew(
            **self.compute_crew_args()
        )

        output = macro_crew.crew().kickoff()
        self.state.macro_planning = output.pydantic
        self.fill_cities_poll()
        self.save_data()


    @listen(or_(initialize, "activities"))
    def find_activities(self):
        current_city = self.state.cities_queue.pop(0)
        input(f"Next step : activities for {current_city}. Press Enter to continue...")
        activity_crew = ActivityCrew(
            **self.compute_crew_args(),
            city=current_city
        )
        output = activity_crew.crew().kickoff()
        self.state.activities.extend(output.pydantic.activities)
        self.save_data()


    @router(find_activities)
    def is_activities_finished(self):
        if self.state.cities_queue:
            return "activities"
        else:
            self.fill_cities_poll()
            return "food"

    @listen("food")
    def find_food(self):
        current_city = self.state.cities_queue.pop(0)
        input(f"Next step : foods for {current_city}. Press Enter to continue...")
        food_crew = FoodCrew(
            **self.compute_crew_args(),
            city=current_city
        )
        output = food_crew.crew().kickoff()
        self.state.foods.extend(output.pydantic.foods)
        self.save_data()


    @router(find_food)
    def is_food_finished(self):
        if self.state.cities_queue:
            return "food"
        else:
            self.fill_cities_poll()
            return "accommodation"

    @listen("accommodation")
    def find_accommodation(self):
        current_city = self.state.cities_queue.pop(0)
        input(f"Next step : accommodations for {current_city}. Press Enter to continue...")
        accommodation_crew = AccommodationCrew(
            **self.compute_crew_args(),
            city=current_city
        )
        output = accommodation_crew.crew().kickoff()
        self.state.accommodations.extend(output.pydantic.accommodations)
        self.save_data()


    @router(find_accommodation)
    def is_accommodations_finished(self):
        if self.state.cities_queue:
            return "accommodation"
        else:
            return "border"


    @listen("border")
    def border_and_customs(self):
        input(f"Next step : border checks. Press Enter to continue...")
        border_crew = BorderCrew(
            **self.compute_crew_args()
        )
        output = border_crew.crew().kickoff()
        self.state.borders.extend(output.pydantic.borders)
        self.save_data()

    def save_data(self):
        with open("output/travel_data.json", "w", encoding="utf-8") as f:
            f.write(self.state.model_dump_json())

    def fill_cities_poll(self):
        self.state.cities_queue = [city.name for city in self.state.macro_planning.ordered_cities]

    def compute_crew_args(self):
        return {
            "original_country": self.state.original_country,
            "destination_country": self.state.destination_country,
            "date": self.state.date,
            "traveler_count": self.state.traveler_count
        }
