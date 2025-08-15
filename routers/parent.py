from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import ParentCreate, ParentUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_users import Parent
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/parent", tags=["parent"])

@router.post("/")
def create_parent(parent: ParentCreate, db: Session = Depends(get_db)):
    new_id = generate_parent_id(db)
    db_parent = Parent(**parent.dict(), id = new_id, role = 'parent')
    db.add(db_parent)
    try:
        db.commit()
        db.refresh(db_parent)
        return {"status": "parent created", "parent": db_parent}
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

    # Apply only provided fields
    for key, value in parent.dict(exclude_none=True).items():
        setattr(db_parent, key, value)

    try:
        db.commit()
        db.refresh(db_parent)  # Optional, if you want updated object returned
        return {"message": "Parent updated successfully", "parent updated": db_parent}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

def generate_parent_id(db: Session):
    last = db.query(Parent).order_by(Parent.id.desc()).first()
    if last:
        last_num = int(last.id[2:])  # Remove 'P' and convert to int
        new_id = f"PA{last_num + 1:04d}"
    else:
        new_id = "PA0001"
    return new_id