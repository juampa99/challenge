from faker import Faker

from random import choice, randint
from string import ascii_uppercase, digits
from pycountry import countries

from models.subject import Subject as SubjectModel
from models.career import Career as CareerModel
from models.lead import Lead as LeadModel

from repository.abstract_repository import AbstractRepository

from database import bind_db

from pytypes import Lead as LeadDTO, Career as CareerDTO, Subject as SubjectDTO

fake = Faker()

def setup_test_environment():
    bind_db(test=True)

def generate_random_string(length: int) -> str:
    return "".join(choice(ascii_uppercase) for i in range(length))


def generate_random_number_string(length: int) -> str:
    return "".join(choice(digits) for i in range(length))

def random_subject():
    return SubjectDTO(
        # Not very representative of the field but it works
        name=fake.name(),
        times_taken=randint(1, 19),
        weekly_hours=randint(1, 199),
    )

def random_career(subject_count: int = 0):
    # Subjects list is always returned empty
    return CareerDTO(
        name=fake.name(),
        inscription_year=randint(1901, 2024),
        subjects=[random_subject() for i in range(subject_count)],
    )

def random_lead(career_count: int = None):
    # Careers list is always returned empty

    if career_count is None:
        career_count = randint(0, 3)

    # Alternate implementation of random country just in case
    country = list(countries)[randint(0, len(countries))].name
    return LeadDTO(
        name=fake.name(),
        email=fake.email(),
        address=fake.address(),
        country=country,
        phone=fake.phone_number(),
        careers=[
            random_career(subject_count=randint(0, 4)) for i in range(career_count)
        ],
    )

class MockLeadRepository(AbstractRepository):

    def __init__(self):
        self.db = {}
        self.curr_id = 1

    def get(self, id: int, lazy: bool):
        return self.db[id]

    def update(self, id: int, lead: dict):
        updated_lead = LeadDTO(**lead)
        self.db[id] = updated_lead 

        return updated_lead

    def create(self, lead: dict):
        created_lead = LeadDTO(**lead)
        created_lead.id = self.curr_id
        self.db[self.curr_id] = created_lead
        self.curr_id += 1

        return created_lead

