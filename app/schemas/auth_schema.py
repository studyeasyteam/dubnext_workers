# api/schemas.py

from pydantic import BaseModel

class RegisterSchema(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str
