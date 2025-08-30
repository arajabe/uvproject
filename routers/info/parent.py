from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import ParentCreate, ParentUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_users import Parent,Student
from sqlalchemy.exc import SQLAlchemyError
from core.database.databsetable.tables_users import UserPasswordNew
from core.model.schema import Password
from core.security.hashing import hash_password, verify_password 


router = APIRouter(prefix="/parent", tags=["parent"])

@router.post("/")
def create_parent(parent: ParentCreate, db: Session = Depends(get_db)):
    new_id = generate_parent_id(db)
    db_parent = Parent(**parent.dict(), id = new_id, role = 'parent', reason = "new entry")
    db.add(db_parent)
    try:
        db.commit()
        db.refresh(db_parent)
        # 🔑 also create password record
        default_pw = "welcome123"  # <-- or student.dateofbirth, or ask in UI
        hashed_pw = hash_password(default_pw)
        db_userpass = UserPasswordNew(id=db_parent.id, role='parent', password=hashed_pw)
        db.add(db_userpass)
        db.commit()
        return {"status": "parent created", "parent": db_parent.id}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.delete("/{parent_id}")
def delete_parent(parent_id: str, db: Session = Depends(get_db)):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(404, "Parent not found")
    db.delete(parent)
    try :
        db.commit()
        return {"status": "deleted", "id": parent_id}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.patch("/{parent_id}")
def update_parent(parent_id: str, parent: ParentUpdate, db: Session = Depends(get_db)):
    db_parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")

    # Apply only provided fields to parent
    for key, value in parent.dict(exclude_none=True).items():
        setattr(db_parent, key, value)

    # If you want to propagate certain fields to students (like fathername, mothername)
    students = db.query(Student).filter(Student.parentid == parent_id).all()
    for student in students:
        for key in ["fathername", "mothername", "parentrelation","address", "city", "pincode", "contactnumber", "email", "occupation"]:
            if key in parent.dict(exclude_none=True):
                setattr(student, key, parent.dict(exclude_none=True)[key])

    try:
        db.commit()
        db.refresh(db_parent)
        for student in students:
            db.refresh(student)
        return {"message": "Parent updated successfully", "parent": db_parent}
    except SQLAlchemyError as e:
        db.rollback()
        response = str(e.__cause__ or e)
        return {"status": response}

def generate_parent_id(db: Session):
    last = db.query(Parent).order_by(Parent.id.desc()).first()
    if last:
        last_num = int(last.id[2:])  # Remove 'P' and convert to int
        new_id = f"PA{last_num + 1:04d}"
    else:
        new_id = "PA0001"
    return new_id