from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import AssignementCreate, AssignementUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_users import Student
from core.database.databsetable.tables_marks import Mark, Assignement
from core.database.databsetable.tables_allocations import StudentClassAllocation
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/assignement", tags=["assignement"])

@router.post("/")
def create_student_assignement(assignement: AssignementCreate, db: Session = Depends(get_db)):
    new_id = generate_assignement_id(db)

    # Fetch student info and class allocation in one query
    result = (
        db.query(
        Student.name,
        StudentClassAllocation.student_class,
        StudentClassAllocation.class_section
        )
        .join(StudentClassAllocation, Student.id == StudentClassAllocation.student_id)
        .filter(Student.id == assignement.student_id)
        .first()
        )

    # Unpack or set defaults
    if result:
        std_name, std_class, std_class_sec = result
    else:
        std_name = std_class = std_class_sec = None

    # Create the Assignement object
    db_assignement = Assignement(**assignement.dict(), id=new_id,
    student_name=std_name, student_class=std_class, class_section=std_class_sec)
    db.add(db_assignement)
    try:
        db.commit()
        db.refresh(db_assignement)
        return {"status": "assignement list created", "created assignement": db_assignement}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.patch("/{student_id}/term/{term}/period/{period}")
def update_student_mark(student_id: str, term: int, period : int, assignement_update: AssignementUpdate, db: Session = Depends(get_db)):
    db_assignement = db.query(Assignement).filter(
        Assignement.student_id == student_id,
        Assignement.term == term,
        Assignement.period == period

    ).first()

    if not db_assignement:
        raise HTTPException(status_code=404, detail="Assignement record not found")
    
    # Extract only provided fields and not None
    update_data = assignement_update.dict(exclude_unset=True, exclude_none=True)

    # Apply changes
    for key, value in update_data.items():
        setattr(db_assignement, key, value)

    try:
        db.commit()
        db.refresh(db_assignement)
        return {"status": "assignement updated", "assignement updated": db_assignement}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.delete("/{student_id}/term/{term}/period/{period}")
def delete_student_mark(student_id: str, period : int, term : int, db: Session = Depends(get_db)):
    db_assignement = db.query(Assignement).filter(
        Assignement.student_id == student_id, Assignement.term == term, Assignement.period == period).first()
  
    if not db_assignement:
        raise HTTPException(404, "student not found")
    db.delete(db_assignement)
    try:
        db.commit()
        return {"status": "deleted assignement list", "student_id": student_id, "term" : term, "period": period}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.get("/{student_id}/{term}")
def delete_student_mark(student_id: str, term : int, db: Session = Depends(get_db)):
    db_mark = db.query(Mark).filter(Mark.student_id == student_id, Mark.term == term).first()
    print("db_mark", db_mark)
    if not db_mark:
        raise HTTPException(404, "student not found")
    get_mark = db.get(db_mark)
    try :
        db.commit()
        return {"status": "deleted mark list", "student mark": get_mark}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

def generate_assignement_id(db: Session):
    last = db.query(Assignement).order_by(Assignement.id.desc()).first()
    if last:
        last_num = int(last.id[1:])  # Remove 'A' and convert to int
        new_id = f"A{last_num + 1:05d}"
    else:
        new_id = "A00001"
    return new_id