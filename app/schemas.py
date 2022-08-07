from pydantic import BaseModel, EmailStr
from typing import Optional


class Workout(BaseModel):
    title: str
    reps: int
    notes: Optional[str] = True


class WorkoutResponse(Workout):
    owner_id: int

    class Config:
        orm_mode = True


class Lifter(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# hide password in response
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
