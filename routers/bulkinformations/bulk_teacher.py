from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.model.schema import BulkTeacher
from core.database.databse import get_db
from sqlalchemy.exc import SQLAlchemyError
from core.database.databsetable.tables_users import Teacher


router = APIRouter(prefix="/teacher", tags=["bulk_teacher"])
    
@router.post("/upload")
def create_bulk_teacher( bulk_data : BulkTeacher, db: Session = Depends(get_db)):

    saved_records = []
    errors = []
    
  
    for record in bulk_data.records:
            
            new_id = generate_teacher_id(db)
            
            db_teacher = Teacher(**record.dict(), id=new_id , role = 'teacher', reason = "New entry")
            db.add(db_teacher)

            try:
                 db.commit()
                 db.refresh(db_teacher)
                 saved_records.append({"teacher id": db_teacher.id, "teacher name": db_teacher.name})
            except SQLAlchemyError as e:
                db.rollback()
                errors.append({"Teacher": f"{record.name} not created", "error": str(e.__cause__ or e)})            
            # saved_records.append(record) 
    return {"reply": {"status": "completed", "errors" : errors if errors else "no error on given data", "saved records" : saved_records}}
 
def generate_teacher_id(db: Session):
    last = db.query(Teacher).order_by(Teacher.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  
        new_id = f"TEA{last_num + 1:04d}"
    else:
        new_id = "TEA0001"
    return new_id