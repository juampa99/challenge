from typing import Optional
from pycountry import countries

from exceptions import InvalidCountryError
from pydantic import BaseModel, Field, field_validator

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
    phone: str = Field(max_length=25)
    careers: list[Career]

    country: str

    # Validates country is a valid country
    @field_validator("country")
    @classmethod
    def ensure_country(cls, c):
        # Throws exception if it doesnt exist
        try:
            return countries.lookup(c).name
        except LookupError:
            raise InvalidCountryError(c)
    
