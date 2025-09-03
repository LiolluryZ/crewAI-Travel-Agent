import glob
import os
import sys
from dotenv import load_dotenv
from langtrace_python_sdk import langtrace

from travel_ai.step5.flow import TravelFlow

load_dotenv()

# langtrace.init(api_key = os.getenv('LANGTRACE_API_KEY'))


def run():
  """
  Run the crew.
  """
  # tool = PassportTool()
  # resultat = tool._run("./input/passport_olivier.jpg")
  # print(resultat)

  result = TravelFlow().kickoff()
  print(result)