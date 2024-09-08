from pony.orm import db_session

from models.lead import Lead as LeadModel
from models.career import Career as CareerModel
from models.subject import Subject as SubjectModel

from pytypes import Lead as LeadDTO
from repository.abstract_repository import AbstractRepository

class LeadRepository(AbstractRepository):
    
    def get(self, id: int, lazy: bool = False) -> LeadDTO:
        with db_session():
            lead = LeadModel.get(id=id)
            if not lazy and lead is not None:
                for career in lead.careers:
                    for subject in career.subjects:
                        pass

        lead_dict = lead.to_dict()
        careers = []
        for c in lead.careers:
            subjects = [s.to_dict for s in c.subjects]
            career_dict = c.to_dict()
            career_dict["subjects"] = [s.to_dict() for s in c.subjects]
            careers.append(career_dict)

        lead_dict["careers"] = careers

        return LeadDTO(**lead_dict)

    def create(self, lead: dict) -> LeadDTO:
        lead_instance = None
        careers = []
        query_careers = lead["careers"]
        with db_session():
            del lead["careers"]

            lead_instance = LeadModel(**lead)

            for career_dict in query_careers:
                subjects_dict = career_dict["subjects"]
                del career_dict["subjects"]

                career_instance = CareerModel(**career_dict, lead=lead_instance)

                for subject in subjects_dict:
                    SubjectModel(**subject, career=career_instance)

        return self.get(lead_instance.id)
    
