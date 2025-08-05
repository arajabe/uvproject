from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import MarkQueryParams, RequestPayload
from core.db.db import get_db, Mark

router = APIRouter(prefix="/performance", tags=["performance"])

@router.post("/")
def get_performance(payload: RequestPayload, db: Session = Depends(get_db)):
    student_id = payload.params.student_id
    subjects = payload.params.subject
    terms = payload.params.term

    # Query database
    query = db.query(Mark).filter(
        Mark.student_id == student_id,
        Mark.term.in_(terms)
    ).all()

    if not query:
        return {"message": "No data found."}

    result = []
    for row in query:
        row_data = {
            "term": row.term,
            "student_id": row.student_id
        }
        for subject in subjects:
            if hasattr(row, subject):
                row_data[subject] = getattr(row, subject)
            else:
                row_data[subject] = "subject not found"
        result.append(row_data)

    print("result performance")
    print(result)

    return {
        "student_id": student_id,
        "results": result
    }