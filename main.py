from http.client import HTTPException
from fastapi import FastAPI, Depends, Path, HTTPException
from sqlalchemy.sql.annotation import Annotated
from typing import Annotated
from models import Base, ToDo
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from routers.auth import router as auth_router
from routers.todo import  auth_router as todo_router
app = FastAPI()
app.include_router(auth_router)
app.include_router(todo_router)

Base.metadata.create_all(engine)



