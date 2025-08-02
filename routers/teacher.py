from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import TeacherCreate, TeacherUpdate
from core.db.db import get_db, Teacher


router = APIRouter(prefix="/teacher", tags=["teacher"])

@router.post("/")
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    print("teacher post")
    db_teacher = Teacher(name=teacher.name, email=teacher.email)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    print("user request post")
    return {"status": "created", "teacher": {"id": db_teacher.id, "name": db_teacher.name}}

@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(404, "teacher not found")
    db.delete(teacher)
    db.commit()
    return {"status": "deleted", "id": teacher_id}

@router.put("/{teacher_id}")
def update_teacher(teacher_id: int, user: TeacherUpdate, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(404, "Teacher not found")
    if user.name: db_teacher.name = user.name
    if user.email: db_teacher.email = user.email
    db.commit()
    return {"status": "updated", "id": db_teacher.id}