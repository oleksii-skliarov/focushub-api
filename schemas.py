from pydantic import BaseModel, ConfigDict, EmailStr


class TaskCreate(BaseModel):
    title: str
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class TaskResponse(TaskCreate):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    tasks: list[TaskResponse] = []

    model_config = ConfigDict(from_attributes=True)