from pydantic import BaseModel

class CheckBorder(BaseModel):
    name: str
    passport_validity: bool
    visa_requirements: bool
    visa_note: str
    customs_regulations: str
    extra_note: str


class CheckBorderList(BaseModel):
    borders: list[CheckBorder]