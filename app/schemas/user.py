from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    email:  str ##EmailStr
    password: str

class UserLogin(BaseModel):
    email: str ##EmailStr
    password: str