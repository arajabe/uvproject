from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import UserCreate, UserUpdate, StudentCreate, StudentUpdate
from core.db.db import get_db, Student


router = APIRouter(prefix="/student", tags=["student"])

@router.post("/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    print("create_student(student: StudentCreate, db: Session = Depends(get_db))")
    db_student = Student(name=student.name, email=student.email)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    print("user request post")
    return {"status": "created", "user": {"id": db_student.id, "name": db_student.name}}

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")
    db.delete(student)
    db.commit()
    return {"status": "deleted", "id": student_id}

@router.put("/{student_id}")
def update_student(student_id: int, user: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(User.id == student_id).first()
    if not db_student:
        raise HTTPException(404, "Student not found")
    if user.name: db_student.name = user.name
    if user.email: db_student.email = user.email
    db.commit()
    return {"status": "updated", "id": db_student.id}