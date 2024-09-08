from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.responses import JSONResponse

from pytypes import Lead
from models.lead import Lead as LeadModel
from repository.abstract_repository import AbstractRepository

class LeadController:

    def __init__(self, lead_repository: AbstractRepository):
        self.router = APIRouter(prefix="/leads")

        self.router.add_api_route(
            "/id/{id}", self.get_lead, methods=["GET"], response_class=JSONResponse
        )
        self.router.add_api_route(
            "/", self.create_lead, methods=["POST"], response_class=JSONResponse
        )

        self.lead_repository = lead_repository

    def get_lead(self, id: int):
        try:
            lead_instance = self.lead_repository.get(id, lazy=False)
        except:
            return JSONResponse(
                content={
                    "detail": [
                        {
                            "msg": "Provided ID doesn't match any stored leads",
                            "input": id,
                        }
                    ]
                },
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return JSONResponse(content=lead_instance.model_dump())

    def create_lead(self, lead: Lead):
        lead = self.lead_repository.create(lead.model_dump())
        return JSONResponse(content=lead.model_dump())
        
