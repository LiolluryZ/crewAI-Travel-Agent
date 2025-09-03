import glob
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool

from travel_ai.step5.crew import TravelCrew
from travel_ai.step5.models.macro_planning import MacroPlanning
from travel_ai.step5.tools.user_input_tool import UserInputTool


@CrewBase
class MacroCrew(TravelCrew):
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

    @task
    def macro_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['macro_planning_task'],
            output_pydantic=MacroPlanning,
            human_input=True,
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
