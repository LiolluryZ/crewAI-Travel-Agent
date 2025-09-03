import glob
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool

from travel_ai.step4.tools.passport_tool import PassportTool
from travel_ai.step4.tools.user_input_tool import UserInputTool


class TravelCrew():
    """TravelCrew crew"""

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
