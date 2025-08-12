from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import SubjectTermSplitCreate
from core.db.db import get_db, SubjectTermSplit,Student


router = APIRouter(prefix="/subjecttermsplit", tags=["subjecttermsplit"])

@router.post("/")
def create_student_subject_term_split(subject_term_split: SubjectTermSplitCreate, db: Session = Depends(get_db)):

    new_id = generate_subject_term_split_id(db)

    std_name = db.query(Student.name).filter(Student.id == subject_term_split.student_id).first()
    if std_name:
        std_name = std_name[0]

    
    db_subject_term_split = SubjectTermSplit(**subject_term_split.dict(), id = new_id, student_name =std_name)


    db_subject_term_split.subject = subject_term_split.subject.capitalize()

    db.add(db_subject_term_split)
    db.commit()
    db.refresh(db_subject_term_split)

    return {"status": "subject split mark list created", "mark_status": {"student_id": db_subject_term_split.student_id, "status": db_subject_term_split.subject_total}}

@router.patch("/{student_id}/{subject}/{term}")
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

    db.commit()
    db.refresh(db_subject_term_split)
    
    return {"status": "split term mark updated", "student_id": student_id, "term": term ,"subject total" : db_subject_term_split.subject_total}

@router.delete("/{student_id}/{subject}/{term}")
def delete_student_subject_term_split(student_id: str, subject : str, term : int, db: Session = Depends(get_db)):
    db_subject_term_split = db.query(SubjectTermSplit).filter(
        SubjectTermSplit.student_id == student_id,
        SubjectTermSplit.term == term,
        SubjectTermSplit.subject == subject
    ).first()

    if not db_subject_term_split:
        raise HTTPException(404, "student not found")
    db.delete(db_subject_term_split)
    db.commit()
    return {"status": "deleted split subject mark list", "student_id": student_id, "term" : term}

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
    db.commit()
    return {"status": "term split mark list", "student_id": student_id, "term" : term, "mark" : get_mark}

def generate_subject_term_split_id(db: Session):
    last = db.query(SubjectTermSplit).order_by(SubjectTermSplit.id.desc()).first()
    if last:
        last_num = int(last.id[1:])  # Remove 'P' and convert to int
        new_id = f"S{last_num + 1:05d}"
    else:
        new_id = "S00001"
    return new_id