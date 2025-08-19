from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.model.schema import BulkClassTeacherAllocation
from core.database.databse import get_db
from core.database.databsetable.tables_allocations import ClassTeacherAllocation
from sqlalchemy.exc import SQLAlchemyError
from core.database.databsetable.tables_users import Teacher



router = APIRouter(prefix="/class_teacher_allocation", tags=["bulk_class_teacher_allocation"])
    
@router.post("/upload")
def create_bulk_class_teacher_allocation( bulk_data : BulkClassTeacherAllocation, db: Session = Depends(get_db)):

    saved_records = []
    errors = []
    
  
    for record in bulk_data.records:
        try:
            teacher = (
                db.query(Teacher)
                .filter(Teacher.id == record.teacher_id)
                .first()
            )
            if not teacher:
                errors.append({"teacher_id": record.teacher_id, "error": "Teacher id not found"})
                continue
            
            new_id = generate_class_teacher_allocation_id(db)
            print(new_id)
            
            db_class_teacher_allocation = ClassTeacherAllocation(
                id=new_id ,
                teacher_id = record.teacher_id,
                teacher_class=record.teacher_class,
                class_section=record.class_section,
                reason = "New Entry",
            )
            db.add(db_class_teacher_allocation)

            try:
                 db.commit()
                 db.refresh(db_class_teacher_allocation)
                 saved_records.append({"class teacher allocation id " : db_class_teacher_allocation.id, "teacher_id": record.teacher_id})
            except SQLAlchemyError as e:
                db.rollback()
                errors.append({"teacher_id": record.teacher_id, "error": str(e.__cause__ or e)})
            
            # saved_records.append(record)

        except SQLAlchemyError as e:
            db.rollback()
            errors.append({
                "student_id": record.teacher_id,
                "error": str(e.__cause__ or e)
            })  
    return {"reply": {"status": "completed", "errors" : errors if errors else "no error on given data", "saved data" : saved_records}}
 
def generate_class_teacher_allocation_id(db: Session):
    last = db.query(ClassTeacherAllocation).order_by(ClassTeacherAllocation.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  # Remove 'P' and convert to int
        new_id = f"CTA{last_num + 1:04d}"
    else:
        new_id = "CTA0001"
    return new_id