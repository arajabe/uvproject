from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import MarkCreate,MarkUpdate
from core.db.db import get_db, Mark, Student


router = APIRouter(prefix="/mark", tags=["mark"])

@router.post("/")
def create_student_mark(mark: MarkCreate, db: Session = Depends(get_db)):
    new_id = generate_parent_id(db)

    std_name = db.query(Student.name).filter(Student.id == mark.student_id).first()
    if std_name:
        std_name = std_name[0]

    db_mark = Mark(**mark.dict(), id = new_id)
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    print("user request post")
    return {"status": "mark list created", "mark_status": {"student_id": db_mark.student_id, "status": db_mark.overall_status}}

@router.patch("/{student_id}/{term}")
def update_student_mark(student_id: str, term: int, mark: MarkUpdate, db: Session = Depends(get_db)):
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
    
    return {"status": "mark updated", "student_id": student_id, "term": term ,"performance" : db_mark.overall_status}

@router.delete("/{student_id}/{term}")
def delete_student_mark(student_id: str, term : int, db: Session = Depends(get_db)):
    db_mark = db.query(Mark).filter(Mark.student_id == student_id, Mark.term == term).first()
    print("db_mark", db_mark)
    if not db_mark:
        raise HTTPException(404, "student not found")
    db.delete(db_mark)
    db.commit()
    return {"status": "deleted mark list", "student_id": student_id, "term" : term}

@router.get("/{student_id}/{term}")
def delete_student_mark(student_id: str, term : int, db: Session = Depends(get_db)):
    db_mark = db.query(Mark).filter(Mark.student_id == student_id, Mark.term == term).first()
    print("db_mark", db_mark)
    if not db_mark:
        raise HTTPException(404, "student not found")
    get_mark = db.get(db_mark)
    db.commit()
    return {"status": "deleted mark list", "student_id": student_id, "term" : term, "mark" : get_mark}

def generate_parent_id(db: Session):
    last = db.query(Mark).order_by(Mark.id.desc()).first()
    if last:
        last_num = int(last.id[1:])  # Remove 'P' and convert to int
        new_id = f"M{last_num + 1:05d}"
    else:
        new_id = "M0001"
    return new_id