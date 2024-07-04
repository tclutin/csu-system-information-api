from pydantic import BaseModel, EmailStr


class RegisterUserDTO(BaseModel):
    username: str
    email: EmailStr
    fullname: str
    role: str
    password: str


class LoginUserDTO(BaseModel):
    username: str
    password: str
