from pydantic import BaseModel, Field, validator
from pycountry import countries
from typing import Optional

EMAIL_REGEX = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"

class Subject(BaseModel):
    name: str = Field(max_length=100)
    times_taken: int = Field(gt=0, lt=20)
    weekly_hours: int = Field(gt=0, lt=200)

class Career(BaseModel):
    name: str = Field(max_length=100)
    inscription_year: int = Field(gt=1900, lt=2500)

    subjects: list[Subject]

class Lead(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=100)
    email: str = Field(pattern=EMAIL_REGEX)
    address: str = Field(max_length=255)
    phone: str = Field(max_length=14)
    careers: list[Career]

    country: str
    # Validates country is a valid country
    @validator('country')
    def ensure_country(cls, c):
        # Throws exception if it doesnt exist
        return countries.lookup(c).name

    @classmethod
    def from_model(cls, model):
        careers = []
        for career in model.careers:
            subjects = [subject.to_dict() for subject in career.subjects]
            career_dict = career.to_dict()
            career_dict["subjects"] = subjects

            careers.append(career_dict)

        lead_dict = model.to_dict()
        lead_dict["careers"] = careers

        return Lead(**lead_dict)

