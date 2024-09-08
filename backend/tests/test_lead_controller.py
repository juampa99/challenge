import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from pony.orm import select, db_session

from logging import getLogger

from utils import setup_test_environment, random_lead, MockLeadRepository
from pytypes import Lead, Career, Subject
from models.lead import Lead as LeadModel

from repository.abstract_repository import AbstractRepository
from controllers.lead_controller import LeadController

logger = getLogger()

setup_test_environment()

@pytest.fixture(scope="function")
def setup():
    app = FastAPI()

    lead_repository = MockLeadRepository()
    lead_controller = LeadController(lead_repository)

    app.include_router(lead_controller.router)

    client = TestClient(app)
    yield client, lead_repository, lead_controller

@pytest.mark.parametrize("career_count", [0, 1, 500, -1, 1000])
def test_get_lead_success(setup, career_count):
    client, lead_repository, lead_controler = setup

    rand_lead = random_lead(career_count=career_count).model_dump()
    created_lead = lead_repository.create(rand_lead)

    response = client.get(f"/leads/id/{1}")

    assert response.status_code == 200
    assert response.json() == created_lead.model_dump()
    assert len(response.json()["careers"]) >= career_count and len(response.json()["careers"]) >= 0

@pytest.mark.parametrize("id", [0, 2, 1000, -1])
def test_get_lead_invalid_id(setup, id):
    client, lead_repository, lead_controler = setup

    rand_lead = random_lead(career_count=1).model_dump()
    created_lead = lead_repository.create(rand_lead)

    response = client.get(f"/leads/id/{id}")

    assert response.status_code == 404

@pytest.mark.parametrize("career_count", [0, 1, 500, -1, 1000])
def test_create_success(setup, career_count):
    client, lead_repository, lead_controler = setup

    rand_lead = random_lead(career_count=career_count).model_dump()
    response = client.post(f"/leads/", json=rand_lead)

    rand_lead['id'] = 1

    assert response.status_code == 200
    assert response.json() == rand_lead

@pytest.mark.parametrize("career_count", [0, 1, 500, -1, 1000])
def test_create_failure(setup, career_count):
    client, lead_repository, lead_controler = setup

    rand_lead = random_lead(career_count=career_count).model_dump()

    rand_lead["email"] = "thisisaninvalidemail"

    response = client.post(f"/leads/", json=rand_lead)

    rand_lead['id'] = 1

    logger.info(response.json())

    assert response.status_code == 422
    assert response.json() != rand_lead
    assert response.json()["detail"][0]["type"] == "string_pattern_mismatch"
    assert response.json()["detail"][0]["loc"] == ['body', 'email']

