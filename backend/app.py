from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.subject import Subject
from models.career import Career
from models.lead import Lead

from database import bind_db

from controllers.lead_controller import LeadController
from services.lead_service import LeadService

lead_service = LeadService()

lead_controler = LeadController(lead_service=lead_service)

bind_db()

app = FastAPI()
app.include_router(lead_controler.router)

