from sqlalchemy.orm import Session
import models
import schemas

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_task_by_id(db: Session, task_id: int, user_id: int):
    return (
        db.query(models.TaskDB)
        .filter(
            models.TaskDB.id == task_id,
            models.TaskDB.owner_id == user_id,
        )
        .first()
    )


def create_new_task(db: Session, task_data: schemas.TaskCreate, user_id: int):
    new_task = models.TaskDB(
        title=task_data.title,
        completed=task_data.completed,
        owner_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# --- ПОЛЬЗОВАТЕЛИ ---
def get_all_users(db: Session):
    return db.query(models.UserDB).all()


def create_new_user(db: Session, user_data: schemas.UserCreate):
    new_user = models.UserDB(username=user_data.username,
                             email=user_data.email,
                             hashed_password = pwd_context.hash(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.UserDB).filter(models.UserDB.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(models.UserDB).filter(models.UserDB.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.UserDB).filter(models.UserDB.email == email).first()

def get_user_tasks(db: Session,
                   user_id: int,
                   limit: int = 10,
                   offset: int = 0,
                   completed: bool | None = None):
    query = db.query(models.TaskDB).filter(models.TaskDB.owner_id == user_id)
    if completed is not None:
        query = query.filter(models.TaskDB.completed == completed)

    return query.offset(offset).limit(limit).all()

def delete_task(db: Session, task_id: int, user_id: int):
    task = (db.query(models.TaskDB)
            .filter(
        models.TaskDB.id == task_id,
                 models.TaskDB.owner_id == user_id
            )
            .first()
            )
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True

def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate, user_id: int):
    task = (db.query(models.TaskDB)
            .filter(
        models.TaskDB.id == task_id,
        models.TaskDB.owner_id == user_id
            )
            .first()
    )
    if not task:
        return None
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.completed is not None:
        task.completed = task_data.completed

    db.commit()
    db.refresh(task)
    return task