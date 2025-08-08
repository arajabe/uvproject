from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import StudentCreate, StudentUpdate
from core.db.db import get_db, Student


router = APIRouter(prefix="/student", tags=["student"])

@router.post("/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_id = generate_student_id(db)
    print("create_student(student: StudentCreate, db: Session = Depends(get_db))")
    db_student = Student(name=student.name, email=student.email, fathername = student.fathername,
                         mothername = student.mothername, dateofbirth = student.dateofbirth, 
                         address =student.address, city = student.city, pincode = student.pincode, 
                         contactnumber = student.contactnumber, aadhar = student.aadhar, id = new_id)

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    print("user request post")
    return {"status": "created", "student": {"id": db_student.id, "name": db_student.name}}

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")
    db.delete(student)
    db.commit()
    return {"status": "deleted", "id": student_id}

@router.put("/{student_id}")
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(404, "Student not found")
    if student.name: db_student.name = student.name
    if student.email: db_student.email = student.email
    db.commit()
    return {"status": "updated", "id": db_student.id}

def generate_student_id(db: Session):
    last = db.query(Student).order_by(Student.id.desc()).first()
    if last:
        last_num = int(last.id[4:])  
        new_id = f"STUD{last_num + 1:04d}"
    else:
        new_id = "STUD0001"
    return new_id