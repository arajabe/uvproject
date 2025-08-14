from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import StudentCreate, StudentUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_users import Student


router = APIRouter(prefix="/student", tags=["student"])

@router.post("/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_id = generate_student_id(db)
    print("create_student(student: StudentCreate, db: Session = Depends(get_db))")
    db_student = Student(** student.dict(), id = new_id, role = "student")

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    print("user request post")
    return {"status": "created", "student": {"id": db_student.id, "name": db_student.name}}

@router.delete("/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")
    db.delete(student)
    db.commit()
    return {"status": "deleted", "id": student_id}

@router.patch("/{student_id}")
def update_student(student_id: str, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student.dict(exclude_unset=True)

    # Apply only provided fields
    for key, value in student.dict(exclude_none=True).items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)

    return {
        "status": "updated",
        "id": db_student.id,
        "updated_fields": list(update_data.keys()),
        "reason": student.reason
    }

def generate_student_id(db: Session):
    last = db.query(Student).order_by(Student.id.desc()).first()
    if last:
        last_num = int(last.id[4:])  
        new_id = f"STUD{last_num + 1:04d}"
    else:
        new_id = "STUD0001"
    return new_id