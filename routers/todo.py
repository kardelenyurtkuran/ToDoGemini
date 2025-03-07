from http.client import HTTPException
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.sql.annotation import Annotated
from typing import Annotated
from models import Base, ToDo
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from routers.auth import router as auth_router

router = APIRouter(
    prefix="/todo",
    tags=["Todo"]
)

class ToDoRequest(BaseModel):
    title: str=Field(min_length=3)
    description: str = Field(min_length=3, max_length=1000)
    priority: int = Field(gt=0, lt=6)
    complete: bool


def get_db():
    db = SessionLocal()
    try:
        yield db #return
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/read_all")
async def read_all(db: db_dependency):
    return db.query(ToDo).all()

@router.get("/get_by_id/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

@router.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency, todo_request: ToDoRequest):
    todo = ToDo(**todo_request.dict()) # tek tek yazmak yerine 2 yıldız (title=todo_request.title, description=todo_request.description)
    db.add(todo)
    db.commit()

@router.put("/update_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency,
                      todo_request: ToDoRequest,
                      todo_id: int = Path(gt=0)
                      ):
    todo = db.query(ToDo).filter(ToDo.id== todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo not found")
    todo.title = todo_request.title
    todo.description =todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete
    db.add(todo)
    db.commit()

@router.delete("/delete_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    db.query(ToDo).filter(ToDo.id==todo_id).delete()
    db.delete(todo)
    db.commit()


