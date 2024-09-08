from database import db
from pony.orm import Required, Set, PrimaryKey


class Career(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, max_len=100)
    inscription_year = Required(int)

    lead = Required("Lead")

    subjects = Set("Subject")

    def to_dict(self, recursive: bool = False, *args, **kwargs):
        if recursive:
            career_dict = super().to_dict(with_collections=True, related_objects=True, *args, **kwargs)
            career_dict["subjects"] = [subj.to_dict() for subj in career_dict["subjects"]]
            for subj in career_dict["subjects"]:
                del subj["career"]
            del career_dict["lead"]
        else:
            career_dict = super().to_dict(*args, **kwargs)

        return career_dict

