from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import TeacherCreate, TeacherUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_users import Teacher
from sqlalchemy.exc import SQLAlchemyError
from core.database.databsetable.tables_users import UserPassword
from core.model.schema import Password
from core.security.hashing import hash_password, verify_password 


router = APIRouter(prefix="/teacher", tags=["teacher"])

@router.post("/")
def create_teacher(teacher: TeacherCreate, db: Session = Depends(get_db)):
    new_id = generate_teacher_id(db)
    db_teacher = Teacher(**teacher.dict(), id = new_id, role = "teacher", reason = "new entry")
    db.add(db_teacher)
    try:
        db.commit()
        db.refresh(db_teacher)
         # 🔑 also create password record
        default_pw = "welcome123"  # <-- or student.dateofbirth, or ask in UI
        hashed_pw = hash_password(default_pw)
        db_userpass = UserPassword(id=db_teacher.id, role='teacher', password=hashed_pw)
        db.add(db_userpass)
        db.commit()
        return {"status": "teacher created", "teacher": db_teacher.id}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: str, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(404, "teacher not found")
    db.delete(teacher)
    try:
        db.commit()
        return {"status": "deleted", "id": teacher_id}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.patch("/{teacher_id}")
def update_teacher(teacher_id: str, teacher: TeacherUpdate, db: Session = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    # Apply only provided fields
    for key, value in teacher.dict(exclude_none=True).items():
        setattr(db_teacher, key, value)
    try:
        db.commit()
        db.refresh(db_teacher)
        return {"message": "Teacher updated successfully", "updated teacher": db_teacher}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

def generate_teacher_id(db: Session):
    last = db.query(Teacher).order_by(Teacher.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  
        new_id = f"TEA{last_num + 1:04d}"
    else:
        new_id = "TEA0001"
    return new_id