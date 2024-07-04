from pydantic import BaseModel


class CreateSpecialtyDTO(BaseModel):
    specialty_name: str
