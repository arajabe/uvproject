from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.model.schema import BulkStudentClassAllocation
from core.database.databse import get_db
from core.database.databsetable.tables_allocations import StudentClassAllocation
from sqlalchemy.exc import SQLAlchemyError
from core.database.databsetable.tables_users import Student



router = APIRouter(prefix="/student_class_allocation", tags=["bulk_student_class_allocation"])
    
@router.post("/upload")
def create_bulk_student_class_allocation( bulk_data : BulkStudentClassAllocation, db: Session = Depends(get_db)):

    saved_records = []
    errors = []
    
  
    for record in bulk_data.records:
        try:
            student = (
                db.query(Student)
                .filter(Student.id == record.student_id)
                .first()
            )
            if not student:
                errors.append({"student_id": record.student_id, "error": "Student id not found"})
                continue
            
            new_id = generate_student_class_allocation_id(db)
            print(new_id)
            
            db_student_class_allocation = StudentClassAllocation(
                id=new_id ,
                student_id = record.student_id,
                student_class=record.student_class,
                class_section=record.class_section,
                reason = "New Entry"

            )
            db.add(db_student_class_allocation)

            try:
                 db.commit()
                 db.refresh(db_student_class_allocation)
                 saved_records.append({"student allocation id": db_student_class_allocation.id, "student id": db_student_class_allocation.student_id})
            except SQLAlchemyError as e:
                db.rollback()
                errors.append({"student_id": record.student_id, "error": str(e.__cause__ or e)})
            
            # saved_records.append(record)

        except SQLAlchemyError as e:
            db.rollback()
            errors.append({
                "student_id": record.student_id,
                "error": str(e.__cause__ or e)
            })  
    return {"reply": {"status": "completed", "errors" : errors if errors else "No error on gicen data", "saved data": saved_records}}
 
def generate_student_class_allocation_id(db: Session):
    last = db.query(StudentClassAllocation).order_by(StudentClassAllocation.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  # Remove 'P' and convert to int
        new_id = f"SCA{last_num + 1:04d}"
    else:
        new_id = "SCA0001"
    return new_id