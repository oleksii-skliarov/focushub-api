from pydantic import BaseModel, EmailStr
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    completed: bool = False



class TaskResponse(TaskCreate):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    tasks: list[TaskResponse] = []

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
