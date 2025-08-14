from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import LoginRequest
from core.database.databse import get_db
from core.database.databsetable.tables_users import Parent

router = APIRouter(prefix="/login", tags=["login"])

# Dummy user store — use DB in production
USERS = {
    "admin_user": {"password": "admin123", "role": "admin"},
    "teacher_user": {"password": "teach123", "role": "teacher"},
    "student_user": {"password": "stud123", "role": "student"},
    "parent_user": {"password": "parent123", "role": "parent"},
}



@router.post("/")
def login(data: LoginRequest):
    user = USERS.get(data.username)
    print(user)
    print(data.password)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": data.username, "role": user["role"]}