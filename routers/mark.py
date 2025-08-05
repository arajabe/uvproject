from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import MarkCreate,MarkUpdate
from core.db.db import get_db, Mark


router = APIRouter(prefix="/mark", tags=["mark"])

@router.post("/")
def create_student_mark(mark: MarkCreate, db: Session = Depends(get_db)):
    print("create_user(user: UserCreate, db: Session = Depends(get_db))")
    db_mark = Mark(student_id=mark.student_id, term = mark.term, language_1=mark.language_1, language_2=mark.language_2, 
                   maths = mark.maths, science = mark.science, social_science = mark.social_science)
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    print("user request post")
    return {"status": "mark list created", "mark_status": {"student_id": db_mark.student_id, "status": db_mark.overall_status}}

@router.patch("/{student_id}/{term}")
def update_student_mark(student_id: int, term: int, mark: MarkUpdate, db: Session = Depends(get_db)):
    db_mark = db.query(Mark).filter(
        Mark.student_id == student_id,
        Mark.term == term
    ).first()

    if not db_mark:
        raise HTTPException(status_code=404, detail="Mark record not found")

    # Only update fields that are not None
    for field, value in mark.dict(exclude_none=True).items():
        setattr(db_mark, field, value)

    db.commit()
    db.refresh(db_mark)
    print("patch called")
    return {"status": "mark updated", "student_id": student_id, "term": term}

@router.delete("/{student_id}/{term}")
def delete_student_mark(student_id: int, term : int, db: Session = Depends(get_db)):
    db_mark = db.query(Mark).filter(Mark.student_id == student_id, Mark.term == term).first()
    print("db_mark", db_mark)
    if not db_mark:
        raise HTTPException(404, "student not found")
    db.delete(db_mark)
    db.commit()
    return {"status": "deleted mark list", "student_id": student_id, "term" : term}

@router.get("/{student_id}/{term}")
def delete_student_mark(student_id: int, term : int, db: Session = Depends(get_db)):
    db_mark = db.query(Mark).filter(Mark.student_id == student_id, Mark.term == term).first()
    print("db_mark", db_mark)
    if not db_mark:
        raise HTTPException(404, "student not found")
    get_mark = db.get(db_mark)
    db.commit()
    return {"status": "deleted mark list", "student_id": student_id, "term" : term, "mark" : get_mark}