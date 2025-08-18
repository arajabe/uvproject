from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import ClassTeacherAllocationCreate, ClassTeacherAllocationUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_allocations import ClassTeacherAllocation
from sqlalchemy.exc import SQLAlchemyError
from core.database.databsetable.tables_users import Teacher


router = APIRouter(prefix="/classteacherallocation", tags=["classteacherallocation"])

@router.post("/")
def create_class_teacher_allocation(class_teacher_allocation: ClassTeacherAllocationCreate, db: Session = Depends(get_db)):
    new_id = generate_class_teacher_allocation_id(db)
    tea_name = db.query(Teacher.name).filter(Teacher.id == class_teacher_allocation.teacher_id).first()
    if tea_name:
        tea_name = tea_name[0]
        db_class_teacher_allocation = ClassTeacherAllocation(**class_teacher_allocation.dict(), id = new_id, teacher_name = tea_name)
        db.add(db_class_teacher_allocation)
        try:
            db.commit()
            db.refresh(db_class_teacher_allocation)
            return {"status": "class teacher allocation created", "class teacher allocation": db_class_teacher_allocation}
        except SQLAlchemyError as e:
            db.rollback()
    # Return the SQL error details
            response =  str(e.__cause__ or e)
            return {"status": response}
    else:
        return {"status": "class teacher not found, class teacher allocation not created"}

@router.delete("/{class_teacher_allocation_id}")
def delete_class_teacher_allocation(class_teacher_allocation_id: str, db: Session = Depends(get_db)):
    db_class_teacher_allocation = db.query(ClassTeacherAllocation).filter(ClassTeacherAllocation.id == class_teacher_allocation_id).first()
    if not db_class_teacher_allocation:
        raise HTTPException(404, "class teacher allocation not found")
    db.delete(db_class_teacher_allocation)
    try :
        db.commit()
        return {"status": "deleted", "id": class_teacher_allocation_id}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.patch("/{class_teacher_allocation_id}")
def update_class_teacher_allocation(class_teacher_allocation_id: str, class_teacher_allocation: ClassTeacherAllocationUpdate, db: Session = Depends(get_db)):
    db_class_teacher_allocation = db.query(ClassTeacherAllocation).filter(ClassTeacherAllocation.id == class_teacher_allocation_id).first()
    if not db_class_teacher_allocation:
        raise HTTPException(status_code=404, detail="class teacher allocation not found")

    # Apply only provided fields
    for key, value in class_teacher_allocation.dict(exclude_none=True).items():
        setattr(db_class_teacher_allocation, key, value)

    try:
        db.commit()
        db.refresh(db_class_teacher_allocation)  # Optional, if you want updated object returned
        return {"message": "db class teacher allocation updated successfully", "db class teacher allocation updated": db_class_teacher_allocation}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

def generate_class_teacher_allocation_id(db: Session):
    last = db.query(ClassTeacherAllocation).order_by(ClassTeacherAllocation.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  # Remove 'P' and convert to int
        new_id = f"CTA{last_num + 1:04d}"
    else:
        new_id = "CTA0001"
    return new_id