from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import StudentCreate, StudentUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_users import Student,Parent
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/student", tags=["student"])

@router.post("/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_id = generate_student_id(db)
    parent = db.query(Parent).filter(Parent.id == student.parentid).first()
    if parent:
        db_student = Student(**student.dict(), id = new_id, fathername = parent.fathername, 
                         mothername = parent.mothername, address = parent.address, city = parent.city, 
                         pincode = parent.pincode, contactnumber = parent.contactnumber,
                         parentrelation = parent.parentrelation, role = "student", reason = "new entry")
        db.add(db_student)
        try:
            db.commit()
            db.refresh(db_student)
            return {"status": "student created", "student": db_student}
        except SQLAlchemyError as e:
            db.rollback()
    # Return the SQL error details
            response =  str(e.__cause__ or e)
            return {"status": response}
    else:
            return {"status" : "parent not found"}

@router.delete("/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(404, "Student not found")
    db.delete(student)
    try:
        db.commit()
        return {"status": "student deleted", "id": student_id}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.patch("/{student_id}")
def update_student(student_id: str, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    # If parentid is provided, validate it
    if student.parentid:
        db_parent = db.query(Parent).filter(Parent.id == student.parentid).first()
        if not db_parent:
            raise HTTPException(status_code=404, detail="Parent not found")

    # Apply only provided student fields (always do this)
    for key, value in student.dict(exclude_none=True).items():
        setattr(db_student, key, value)

    # If parent is linked, sync fields from parent → student
    if student.parentid:
        parent_fields = [
            "fathername", "mothername", "parentrelation",
            "address", "city", "pincode", "contactnumber", "email"
        ]
        for key in parent_fields:
            if hasattr(db_parent, key):
                setattr(db_student, key, getattr(db_parent, key))

    try:
        db.commit()
        db.refresh(db_student)
        return {
            "status": "student updated",
            "updated_student": student.dict(exclude_none=True)  # return updated fields only
        }
    except SQLAlchemyError as e:
        db.rollback()
        response = str(e.__cause__ or e)
        raise HTTPException(status_code=500, detail=response)

def generate_student_id(db: Session):
    last = db.query(Student).order_by(Student.id.desc()).first()
    if last:
        last_num = int(last.id[4:])  
        new_id = f"STUD{last_num + 1:04d}"
    else:
        new_id = "STUD0001"
    return new_id