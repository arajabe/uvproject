from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import SubjectTermSplitCreate
from core.database.databse import get_db
from core.database.databsetable.tables_marks import SubjectTermSplit
from core.database.databsetable.tables_allocations import StudentClassAllocation
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/subjecttermsplit", tags=["subjecttermsplit"])

@router.post("/")
def create_student_subject_term_split(subject_term_split: SubjectTermSplitCreate, db: Session = Depends(get_db)):

    new_id = generate_subject_term_split_id(db)

    std_cls_allo = ( db.query(StudentClassAllocation)
                           .filter(StudentClassAllocation.student_id == subject_term_split.student_id)
                        .first())

    if not std_cls_allo:
            return {"status": "Student class has not been allocated in the class"}
    else:

        db_subject_term_split = SubjectTermSplit(**subject_term_split.dict(), id=new_id)

        # Ensure subject name is properly formatted
        db_subject_term_split.subject = subject_term_split.subject.title()

        db.add(db_subject_term_split)

        try:
            db.commit()
            db.refresh(db_subject_term_split)
            return {"status": "subject split mark list created","mark": db_subject_term_split,}
        except SQLAlchemyError as e:
            db.rollback()
            return {"status": str(e.__cause__ or e)}




@router.patch("/student/{student_id}/subject/{subject}/term/{term}")
def update_student_subject_term_split(student_id: str, term: int, subject : str, subject_term_split: SubjectTermSplitCreate, db: Session = Depends(get_db)):
    db_subject_term_split = db.query(SubjectTermSplit).filter(
        SubjectTermSplit.student_id == student_id,
        SubjectTermSplit.term == term,
        SubjectTermSplit.subject == subject
    ).first()

    if not db_subject_term_split:
        raise HTTPException(status_code=404, detail="Mark record not found")

    subject_term_split.subject = subject_term_split.subject.capitalize()
    # Only update fields that are not None
    for field, value in subject_term_split.dict(exclude_none=True).items():
        setattr(db_subject_term_split, field, value)
    try:
        db.commit()
        db.refresh(db_subject_term_split)    
        return {"status": "split term mark updated", "updated split term mark" : db_subject_term_split}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.delete("/student/{student_id}/subject/{subject}/term/{term}")
def delete_student_subject_term_split(student_id: str, subject : str, term : int, db: Session = Depends(get_db)):
    db_subject_term_split = db.query(SubjectTermSplit).filter(
        SubjectTermSplit.student_id == student_id,
        SubjectTermSplit.term == term,
        SubjectTermSplit.subject == subject
    ).first()

    if not db_subject_term_split:
        raise HTTPException(404, "student not found")
    db.delete(db_subject_term_split)
    try:
        db.commit()
        return {"status": "deleted split subject mark list", "student_id": student_id, "term" : term}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.get("/{student_id}/subject/{term}")
def delete_student_subject_term_split(student_id: str, subject : str, term : int, db: Session = Depends(get_db)):
    db_subject_term_split = db.query(SubjectTermSplit).filter(
        SubjectTermSplit.student_id == student_id,
        SubjectTermSplit.term == term,
        SubjectTermSplit.subject == subject
    ).first()
    print("db_mark", db_subject_term_split)
    if not db_subject_term_split:
        raise HTTPException(404, "student not found")
    get_mark = db.get(db_subject_term_split)
    try:
        db.commit()
        return {"status": "term split mark list", "student_id": student_id, "term" : term, "mark" : get_mark}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

def generate_subject_term_split_id(db: Session):
    last = db.query(SubjectTermSplit).order_by(SubjectTermSplit.id.desc()).first()
    if last:
        last_num = int(last.id[1:])  # Remove 'P' and convert to int
        new_id = f"S{last_num + 1:05d}"
    else:
        new_id = "S00001"
    return new_id