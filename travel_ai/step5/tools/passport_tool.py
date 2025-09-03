import os
from crewai.tools import BaseTool
from datetime import datetime
from passporteye import read_mrz
from pydantic import BaseModel, Field
from typing import Type


class PassportToolInput(BaseModel):
    name: str = Field(description="Name of passenger")

class PassportTool(BaseTool):
    name: str = "passport_tool"
    description: str = "Read passport from an image."
    args_schema: Type[BaseModel] = PassportToolInput

    def format_date(self, date_str: str) -> str:
        if len(date_str) != 6 or not date_str.isdigit():
            raise ValueError("Le format doit être YYMMDD, par exemple '881119'")

        # Extraire les parties
        yy = int(date_str[:2])
        mm = int(date_str[2:4])
        dd = int(date_str[4:6])

        yyyy = 1900 + yy if yy >= 50 else 2000 + yy

        date_obj = datetime(yyyy, mm, dd)
        return date_obj.strftime("%m/%d/%Y")

    def _run(self, name: str):
        """
        Use passporteye to read MRZ from an image.
        """
        file = f"input/{name}.jpg"
        # Check if the file exists
        if not os.path.exists(file):
            raise FileNotFoundError(f"The file {file} does not exist.")

        mrz = read_mrz(file, save_roi=True)

        return {
            "date_of_birth": self.format_date(mrz.date_of_birth),
            "expiration_date": self.format_date(mrz.expiration_date),
            "nationality": mrz.nationality,
            "sex": mrz.sex
        }
