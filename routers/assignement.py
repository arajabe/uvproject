from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import AssignementCreate, AssignementUpdate, AssignementDelete
from core.db.db import get_db, Mark, Student, Assignement


router = APIRouter(prefix="/assignement", tags=["assignement"])

@router.post("/")
def create_student_assignement(assignement: AssignementCreate, db: Session = Depends(get_db)):
    new_id = generate_assignement_id(db)

    std_name = db.query(Student.name).filter(Student.id == assignement.student_id).first()
    if std_name:
        std_name = std_name[0]

    db_assignement = Assignement(**assignement.dict(), id = new_id)
    db.add(db_assignement)
    db.commit()
    db.refresh(db_assignement)
    print("user request post")
    return {"status": "assignement list created", "assignement_status": {"student_id": db_assignement.student_id}}

@router.patch("/{student_id}/term/{term}/period/{period}")
def update_student_mark(student_id: str, term: int, period : int, assignement_update: AssignementUpdate, db: Session = Depends(get_db)):
    db_assignement = db.query(Assignement).filter(
        Assignement.student_id == student_id,
        Assignement.term == term,
        Assignement.period == period

    ).first()

    if not db_assignement:
        raise HTTPException(status_code=404, detail="Assignement record not found")

    # Only update fields that are not None
    for field, value in assignement_update.dict(exclude_none=True).items():
        setattr(db_assignement, field, value)

    db.commit()
    db.refresh(db_assignement)
    
    return {"status": "assignement updated", "student_id": student_id, "term": term }

@router.delete("/{student_id}/term/{term}/period/{period}")
def delete_student_mark(student_id: str, period : int, term : int, db: Session = Depends(get_db)):
    db_assignement = db.query(Assignement).filter(
        Assignement.student_id == student_id, Assignement.term == term, Assignement.period == period).first()
  
    if not db_assignement:
        raise HTTPException(404, "student not found")
    db.delete(db_assignement)
    db.commit()
    return {"status": "deleted assignement list", "student_id": student_id, "term" : term, "period": period}

@router.get("/{student_id}/{term}")
def delete_student_mark(student_id: str, term : int, db: Session = Depends(get_db)):
    db_mark = db.query(Mark).filter(Mark.student_id == student_id, Mark.term == term).first()
    print("db_mark", db_mark)
    if not db_mark:
        raise HTTPException(404, "student not found")
    get_mark = db.get(db_mark)
    db.commit()
    return {"status": "deleted mark list", "student_id": student_id, "term" : term, "mark" : get_mark}

def generate_assignement_id(db: Session):
    last = db.query(Assignement).order_by(Assignement.id.desc()).first()
    if last:
        last_num = int(last.id[1:])  # Remove 'A' and convert to int
        new_id = f"A{last_num + 1:05d}"
    else:
        new_id = "A00001"
    return new_id