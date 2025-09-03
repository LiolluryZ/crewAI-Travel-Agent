import glob
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import DirectorySearchTool, FileReadTool, DirectoryReadTool


@CrewBase
class TravelCrew():
    """TravelCrew crew"""

    def __init__(self, original_country, destination_country):
        self.original_country = original_country
        self.destination_country = destination_country
        pass

    @before_kickoff
    def prepare_inputs(self, inputs):
        inputs['original_country'] = self.original_country
        inputs['destination_country'] = self.destination_country
        return inputs

    @agent
    def macro_trip_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['macro_trip_planner'],
            verbose=True,
            tools=[
            ]
        )

    @agent
    def activity_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['activity_planner'],
            verbose=True,
            tools=[
            ]
        )

    @agent
    def food_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['food_planner'],
            verbose=True,
            tools=[
            ]
        )

    @agent
    def accommodation_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['accommodation_planner'],
            verbose=True,
            tools=[
            ]
        )

    @task
    def macro_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['macro_planning_task'],
            output_file=f'step1_output/macro_planning.md'
        )

    @task
    def activity_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['activity_planning_task'],
            output_file=f'step1_output/activity_planning.md'
        )

    @task
    def food_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['food_research_task'],
            output_file=f'step1_output/food_research.md'
        )

    @task
    def accommodation_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['accommodation_planning_task'],
            output_file=f'step1_output/accommodation_planning.md'
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
