import glob
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool

from travel_ai.step5.crew import TravelCrew
from travel_ai.step5.models.food import FoodList
from travel_ai.step5.tools.user_input_tool import UserInputTool


@CrewBase
class FoodCrew(TravelCrew):
    """TravelCrew crew"""


    def __init__(self, original_country, destination_country, date, traveler_count, city):
        self.original_country = original_country
        self.destination_country = destination_country
        self.date = date
        self.traveler_count = traveler_count
        self.city = city

    @before_kickoff
    def prepare_inputs(self, inputs):
        inputs['original_country'] = self.original_country
        inputs['destination_country'] = self.destination_country
        inputs['date'] = self.date
        inputs['traveler_count'] = self.traveler_count
        inputs['city'] = self.city
        return inputs

    @agent
    def food_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['food_planner'],
            verbose=True,
            tools=[
                SerperDevTool(),
                UserInputTool(),
                ScrapeWebsiteTool()
            ]
        )

    @task
    def food_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['food_research_task'],
            output_pydantic=FoodList
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TravelCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
