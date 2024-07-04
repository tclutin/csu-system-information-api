from pydantic import BaseModel, EmailStr


class CreateDepartmentDTO(BaseModel):
    department_name: str
