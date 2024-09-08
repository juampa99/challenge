from os import environ

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models.subject import Subject
from models.career import Career
from models.lead import Lead

from database import bind_db

from controllers.lead_controller import LeadController
from repository.lead_repository import LeadRepository

from exceptions import InvalidCountryError

lead_controler = LeadController(lead_repository=LeadRepository())

is_test = environ['environment'] =='test' if 'environment' in environ else False
bind_db(test=is_test)

app = FastAPI()

@app.exception_handler(InvalidCountryError)
async def value_error_exception_handler(request, exc: InvalidCountryError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": [
                {
                    "msg": str(exc),
                }
            ]
        },
    )

app.include_router(lead_controler.router)

