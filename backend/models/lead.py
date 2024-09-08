from database import db
from pony.orm import Required, Set, PrimaryKey


class Lead(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, max_len=100)

    # These fields should be validated
    email = Required(str, max_len=320)
    address = Required(str, max_len=100)
    country = Required(str, max_len=100)
    phone = Required(str)

    careers = Set("Career")

    def to_dict(self, recursive: bool = False, remove_ids=False, *args, **kwargs):
        if recursive:
            lead_dict = super().to_dict(with_collections=True, related_objects=True, *args, **kwargs)
            lead_dict["careers"] = [c.to_dict(recursive=True, *args, **kwargs) for c in lead_dict["careers"]]
            del lead_dict["id"]
            if remove_ids:
                for c in lead_dict["careers"]:
                    del c["id"]
                    for s in c["subjects"]:
                        del s["id"]
        else:
            lead_dict = super().to_dict(*args, **kwargs)

        return lead_dict

