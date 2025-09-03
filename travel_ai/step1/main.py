import glob
import os
import sys
from dotenv import load_dotenv
from langtrace_python_sdk import langtrace

from travel_ai.step1.crew import TravelCrew

load_dotenv()

# langtrace.init(api_key = os.getenv('LANGTRACE_API_KEY'))


def run():
  """
  Run the crew.
  """
  TravelCrew(
    original_country='France',
    destination_country='Vietnam',
  ).crew().kickoff()
