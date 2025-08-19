from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.model.schema import BulkStudent
from core.database.databse import get_db
from sqlalchemy.exc import SQLAlchemyError
from core.database.databsetable.tables_users import  Student


router = APIRouter(prefix="/student", tags=["bulk_student"])
    
@router.post("/upload")
def create_bulk_student( bulk_data : BulkStudent, db: Session = Depends(get_db)):

    saved_records = []
    errors = []    
  
    for record in bulk_data.records:
            
            new_id = generate_student_id(db)
            
            db_student = Student(**record.dict(), id=new_id, role = "student")
            db.add(db_student)

            try:
                 db.commit()
                 db.refresh(db_student)
                 saved_records.append(record)
            except SQLAlchemyError as e:
                db.rollback()
                errors.append({"student": record.name, "error": str(e.__cause__ or e)})            
            # saved_records.append(record) 
    return {"reply": {"status": "completed", "errors" : errors}}
 
def generate_student_id(db: Session):
    last = db.query(Student).order_by(Student.id.desc()).first()
    if last:
        last_num = int(last.id[4:])  
        new_id = f"STUD{last_num + 1:04d}"
    else:
        new_id = "STUD0001"
    return new_id