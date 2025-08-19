from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.model.schema import BulkSubjectTermSplit, SubjectTermSplitCreate
from core.database.databse import get_db
from core.database.databsetable.tables_marks import Mark, SubjectTermSplit
from core.database.databsetable.tables_allocations import StudentClassAllocation
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/subject_term_split", tags=["bulk_subjecttermsplit"])
    
@router.post("/upload")
def create_bulk_subject_term_split(bulk_data : BulkSubjectTermSplit, db: Session = Depends(get_db)):

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
            
            new_id = generate_subject_term_split_id(db)
            print(new_id)
            
            db_subject_term_split = SubjectTermSplit(
                id=new_id ,
                student_id=record.student_id,
                term=record.term,
                subject=record.subject,
                mark_section_A=record.mark_section_A,
                mark_section_B=record.mark_section_B,
                mark_section_C=record.mark_section_C,
                mark_section_D=record.mark_section_D,
                abscent=record.abscent,
            )
            db.add(db_subject_term_split)

            try:
                 db.commit()
                 db.refresh(db_subject_term_split)
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
 
def generate_subject_term_split_id(db: Session):
    last = db.query(SubjectTermSplit).order_by(SubjectTermSplit.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  # Remove 'A' and convert to int
        new_id = f"STS{last_num + 1:07d}"
    else:
        new_id = "STS0000001"
    return new_id