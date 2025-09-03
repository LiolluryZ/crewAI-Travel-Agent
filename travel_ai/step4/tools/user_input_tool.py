import os
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type


class UserInputToolInput(BaseModel):
    query: str = Field(description="Query to ask to user.")

class UserInputTool(BaseTool):
    name: str = "user_input_tool"
    description: str = "Ask a question to the user and return the answer."
    args_schema: Type[BaseModel] = UserInputToolInput


    def _run(self, query: str):
        """
        Ask a question to the user and return the answer.
        """
        # Check if the query is empty
        if not query:
            raise ValueError("Query cannot be empty.")

        # Ask the question to the user
        answer = input(f"{query}\n\nRéponse : \n")

        # Check if the answer is empty
        if not answer:
            raise ValueError("Answer cannot be empty.")

        return answer