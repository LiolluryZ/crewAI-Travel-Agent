import glob
import os
import sys
from dotenv import load_dotenv
from langtrace_python_sdk import langtrace

from travel_ai.step4.crew import TravelCrew

load_dotenv()

# langtrace.init(api_key = os.getenv('LANGTRACE_API_KEY'))


def run():
  """
  Run the crew.
  """
  # tool = PassportTool()
  # resultat = tool._run("./input/passport_olivier.jpg")
  # print(resultat)

  result = TravelCrew(
    original_country='France',
    destination_country='Vietnam',
    date='2025',
    traveler_count=2
  ).crew().kickoff()
  print(result)