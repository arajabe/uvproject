from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import MarkCreate,MarkUpdate
from core.db.db import get_db, Mark

router = APIRouter(prefix="/performance", tags=["performance"])

@router.post("/")
def get_selected_subject_marks(payload: dict, db: Session = Depends(get_db)):
    params = payload.get("params", {})
    student_id = params.get("student_id")
    subjects = params.get("subject", [])
    terms = params.get("term", [])

    if not student_id or not subjects or not terms:
        raise HTTPException(400, detail="student_id, subject, and term are required.")

    # Query all matching records
    query = db.query(Mark).filter(
        Mark.student_id == student_id,
        Mark.term.in_(terms)
    ).all()

    if not query:
        raise HTTPException(404, detail="No mark records found.")

    # Build filtered response
    results = []
    for row in query:
        result = {
            "term": row.term,
            "student_id": row.student_id
        }
        for sub in subjects:
            if hasattr(row, sub):
                result[sub] = getattr(row, sub)
            else:
                result[sub] = "subject not found"
        results.append(result)

    return {"results": results}