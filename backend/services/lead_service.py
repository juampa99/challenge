from pony.orm import db_session, select
from pytypes import Lead, Career, Subject
from typing import Optional

from models.subject import Subject as SubjectModel
from models.career import Career as CareerModel
from models.lead import Lead as LeadModel

class LeadService():

    @db_session
    def get_lead(self, id: int, lazy=True) -> Optional[LeadModel]:
        lead = LeadModel.get(id=id)
        if not lazy and lead is not None:
            for career in lead.careers:
                for subject in career.subjects:
                    pass
        return lead

    @db_session
    def create_lead(self, lead: Lead) -> LeadModel:
        lead_dict = lead.dict()
        del lead_dict["careers"]

        lead_instance = LeadModel(**lead_dict)

        careers = []
        for career in lead.careers:
            career_dict = career.dict()
            subjects_dict = career_dict["subjects"]
            del career_dict["subjects"]

            career_instance = CareerModel(**career_dict, lead=lead_instance)

            for subject in subjects_dict:
                SubjectModel(**subject, career=career_instance)

        return lead_instance

