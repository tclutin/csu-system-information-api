from pydantic import BaseModel


class CreateGroupDTO(BaseModel):
    department: str
    specialty: str
    shortname: str

