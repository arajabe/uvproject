from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.model.schema import RequestPayload
from core.database.databse import get_db
from core.database.databsetable.tables_marks import Mark
from sqlalchemy.exc import SQLAlchemyError

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

    return {
        "student_id": student_id,
        "results": result
    }