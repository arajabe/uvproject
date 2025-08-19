from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.model.schema import BulkTermMark
from core.database.databse import get_db
from core.database.databsetable.tables_marks import Mark
from core.database.databsetable.tables_allocations import StudentClassAllocation
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/term_mark", tags=["bulk_term_mark"])
    
@router.post("/upload")
def create_bulk_subject_term_split(bulk_data : BulkTermMark, db: Session = Depends(get_db)):

    saved_records = []
    errors = []
    
  
    for record in bulk_data.records:
        try:
            std_cls_allo = (
                db.query(StudentClassAllocation)
                .filter(StudentClassAllocation.student_id == record.student_id)
                .first()
            )
            if not std_cls_allo:
                errors.append({"student_id": record.student_id, "error": "Student not allocated"})
                continue
            
            new_id = generate_mark_id(db)
            print(new_id)
            
            db_mark = Mark(
                id=new_id ,
                student_id=record.student_id,
                term=record.term,
                language_1 = record.language_1,
                language_2 = record.language_2,
                maths=record.maths,
                science=record.science,
                social_science=record.social_science,
            )
            db.add(db_mark)

            try:
                 db.commit()
                 db.refresh(db_mark)
                 saved_records.append(record)
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
    return {"reply": {"status": "completed", "errors" : errors}}
 
def generate_mark_id(db: Session):
    last = db.query(Mark).order_by(Mark.id.desc()).first()
    if last:
        last_num = int(last.id[1:])  # Remove 'P' and convert to int
        new_id = f"M{last_num + 1:05d}"
    else:
        new_id = "M0001"
    return new_id