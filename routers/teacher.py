from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import TeacherCreate, TeacherUpdate
from core.db.db import get_db, Teacher


router = APIRouter(prefix="/teacher", tags=["teacher"])

@router.post("/")
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    new_id = generate_teacher_id(db)
    db_teacher = Teacher(name=teacher.name, email=teacher.email, fathername = teacher.fathername,
                         mothername = teacher.mothername, dateofbirth = teacher.dateofbirth, 
                         address =teacher.address, city = teacher.city, pincode = teacher.pincode, 
                         contactnumber = teacher.contactnumber, aadhar = teacher.aadhar, id = new_id, reason = teacher.reason,
                         graduatedegree = teacher.graduatedegree, subject = teacher.subject, role = "teacher"
                         )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    print("user request post")
    return {"status": "created", "teacher": {"id": db_teacher.id, "name": db_teacher.name}}

@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: str, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(404, "teacher not found")
    db.delete(teacher)
    db.commit()
    return {"status": "deleted", "id": teacher_id}

@router.patch("/{teacher_id}")
def update_teacher(teacher_id: str, teacher: TeacherUpdate, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Apply only provided fields
    for key, value in teacher.dict(exclude_none=True).items():
        setattr(db_teacher, key, value)

    db.commit()
    db.refresh(db_teacher)

    return {"message": "Teacher updated successfully", "data": db_teacher}

def generate_teacher_id(db: Session):
    last = db.query(Teacher).order_by(Teacher.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  
        new_id = f"TEA{last_num + 1:04d}"
    else:
        new_id = "TEA0001"
    return new_id