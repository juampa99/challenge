from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.responses import JSONResponse

from pytypes import Lead
from models.lead import Lead as LeadModel
from services.lead_service import LeadService

class LeadController:
    
    def __init__(self, lead_service: LeadService):
        self.router = APIRouter(prefix="/leads")

        self.router.add_api_route("/id/{id}", self.get_lead, methods=["GET"])
        self.router.add_api_route("/", self.create_lead, methods=["POST"])

        self.lead_service = lead_service
    
    def get_lead(self, id: int):
        lead_instance = self.lead_service.get_lead(id, lazy=False)
        if lead_instance is None:
            return JSONResponse(content={"detail": [{"msg": "Provided ID doesn't match any stored leads", "input":id}]}, status_code=status.HTTP_404_NOT_FOUND)

        return JSONResponse(content=Lead.from_model(lead_instance).dict()) 

    def create_lead(self, lead: Lead):
        lead = self.lead_service.create_lead(lead)
        return Lead.from_model(lead).dict()

