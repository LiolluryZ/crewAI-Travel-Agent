import glob
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool

from travel_ai.step4.models.accommodation import AccommodationList
from travel_ai.step4.models.activity import ActivityList
from travel_ai.step4.models.check_border import CheckBorderList
from travel_ai.step4.models.food import FoodList
from travel_ai.step4.models.macro_planning import MacroPlanning
from travel_ai.step4.tools.passport_tool import PassportTool
from travel_ai.step4.tools.user_input_tool import UserInputTool


@CrewBase
class TravelCrew():
    """TravelCrew crew"""

    def __init__(self, original_country, destination_country, date, traveler_count):
        self.original_country = original_country
        self.destination_country = destination_country
        self.date = date
        self.traveler_count = traveler_count
        pass

    @before_kickoff
    def prepare_inputs(self, inputs):
        inputs['original_country'] = self.original_country
        inputs['destination_country'] = self.destination_country
        inputs['date'] = self.date
        inputs['traveler_count'] = self.traveler_count
        return inputs

    @agent
    def macro_trip_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['macro_trip_planner'],
            verbose=True,
            tools=[
                SerperDevTool(),
                UserInputTool(),
                ScrapeWebsiteTool()
            ]
        )

    @agent
    def activity_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['activity_planner'],
            verbose=True,
            tools=[
                SerperDevTool(),
                UserInputTool(),
                ScrapeWebsiteTool()
            ]
        )

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

    @agent
    def accommodation_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['accommodation_planner'],
            verbose=True,
            tools=[
                SerperDevTool(),
                UserInputTool(),
                ScrapeWebsiteTool()
            ]
        )

    @agent
    def border_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['border_agent'],
            verbose=True,
            tools=[
                SerperDevTool(),
                UserInputTool(),
                ScrapeWebsiteTool(),
                PassportTool()
            ]
        )

    @task
    def macro_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['macro_planning_task'],
            output_pydantic=MacroPlanning,
            output_file=f'step4_output/macro_planning.json'
        )

    @task
    def activity_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['activity_planning_task'],
            output_pydantic=ActivityList,
            output_file=f'step4_output/activity_planning.json'
        )

    @task
    def food_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['food_research_task'],
            output_pydantic=FoodList,
            output_file=f'step4_output/food_research.json'
        )

    @task
    def accommodation_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['accommodation_planning_task'],
            output_pydantic=AccommodationList,
            output_file=f'step4_output/accommodation_planning.json'
        )

    @task
    def check_border_task(self) -> Task:
        return Task(
            config=self.tasks_config['check_border_task'],
            output_pydantic=CheckBorderList,
            output_file=f'step4_output/border.json'
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
