from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import StudentClassAllocationCreate, StudentClassAllocationUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_allocations import StudentClassAllocation
from core.database.databsetable.tables_users import Student
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/studentclassallocation", tags=["studentclassallocation"])

@router.post("/")
def create_student_class_allocation(student_class_allocation: StudentClassAllocationCreate, db: Session = Depends(get_db)):
    new_id = generate_student_class_allocation_id(db)
    std_name = db.query(Student.name).filter(Student.id == student_class_allocation.student_id).first()
    if std_name:
        std_name = std_name[0]
        db_student__class_allocation = StudentClassAllocation(**student_class_allocation.dict(), id = new_id, reason = "New entry")
        db.add(db_student__class_allocation)
        try:
            db.commit()
            db.refresh(db_student__class_allocation)
            return {"status": "student class allocation", "student class allocation": db_student__class_allocation}
        except SQLAlchemyError as e:
            db.rollback()
    # Return the SQL error details
            response =  str(e.__cause__ or e)
            return {"status": response}
    else:
        return {"status" : "Student not found, class not allocated for student"}

@router.delete("/{student_class_allocation_id}")
def delete_student_class_allocation(student_class_allocation_id: str, db: Session = Depends(get_db)):
    db_student__class_allocation = db.query(StudentClassAllocation).filter(StudentClassAllocation.id == student_class_allocation_id).first()
    if not db_student__class_allocation:
        raise HTTPException(404, "student class allocation not found")
    db.delete(db_student__class_allocation)
    try :
        db.commit()
        return {"status": "deleted", "id": student_class_allocation_id}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.patch("/{student_class_allocation_id}")
def update_student_class_allocation(student_class_allocation_id: str, student_class_allocation: StudentClassAllocationUpdate, db: Session = Depends(get_db)):
    db_student_class_allocation = db.query(StudentClassAllocation).filter(StudentClassAllocation.id == student_class_allocation_id).first()
    if not db_student_class_allocation:
        raise HTTPException(status_code=404, detail="student class allocation not found in our data")

    # Apply only provided fields
    for key, value in student_class_allocation.dict(exclude_none=True).items():
        setattr(db_student_class_allocation, key, value)

    try:
        db.commit()
        db.refresh(db_student_class_allocation)  # Optional, if you want updated object returned
        return {"message": "Student class allocation updated successfully", "Student class updated": db_student_class_allocation}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

def generate_student_class_allocation_id(db: Session):
    last = db.query(StudentClassAllocation).order_by(StudentClassAllocation.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  # Remove 'P' and convert to int
        new_id = f"SCA{last_num + 1:04d}"
    else:
        new_id = "SCA0001"
    return new_id