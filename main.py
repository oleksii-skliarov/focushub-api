from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import models
import schemas
import crud
from database import engine, get_db
import auth




app = FastAPI(title="FocusHub API (Jira-like)")

@app.get("/tasks", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db),
              current_user: models.UserDB = Depends(auth.get_current_user),
              limit: int = Query(default=10,ge=1,le=100),
              offset: int = Query(default=0,ge=0),
              completed: bool | None = None):
    return crud.get_user_tasks(db, current_user.id,limit,offset,completed)

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int,
        db: Session = Depends(get_db),
        current_user: models.UserDB = Depends(auth.get_current_user)):
    task = crud.get_task_by_id(db, task_id,current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", status_code=201, response_model=schemas.TaskResponse)
def create_task(
        task_data: schemas.TaskCreate,
        db: Session = Depends(get_db),
        current_user: models.UserDB = Depends(auth.get_current_user)):
    return crud.create_new_task(db, task_data, current_user.id)


@app.post("/users", status_code=201, response_model=schemas.UserResponse)
def create_user(user_data: schemas.UserCreate,
        db: Session = Depends(get_db)):
    if (crud.get_user_by_email(db, user_data.email) is not None
            or crud.get_user_by_username(db, user_data.username) is not None):
        raise HTTPException(status_code=400, detail="Email or username already registered")
    return crud.create_new_user(db, user_data)


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@app.post("/token")
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.UserDB = Depends(auth.get_current_user)):
    return current_user


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int,
                db: Session = Depends(get_db),
                current_user: models.UserDB = Depends(auth.get_current_user)):
    success = crud.delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None

@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
        task_id: int,
        task_data: schemas.TaskUpdate,
        db: Session = Depends(get_db),
        current_user: models.UserDB = Depends(auth.get_current_user),
        ):
    updated_task = crud.update_task(db, task_id, task_data, current_user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task