from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import ParentCreate, ParentUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_users import Parent


router = APIRouter(prefix="/parent", tags=["parent"])

@router.post("/")
def create_parent(parent: ParentCreate, db: Session = Depends(get_db)):
    print(" i am parent post")
    new_id = generate_parent_id(db)
    db_parent = Parent(**parent.dict(), id = new_id, role = 'parent')
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    print("user request post")
    return {"status": "created", "parent": {"id": db_parent.id, "name": db_parent.name}}

@router.delete("/{parent_id}")
def delete_parent(parent_id: str, db: Session = Depends(get_db)):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(404, "Parent not found")
    db.delete(parent)
    db.commit()
    return {"status": "deleted", "id": parent_id}

@router.patch("/{parent_id}")
def update_parent(parent_id: str, parent: ParentUpdate, db: Session = Depends(get_db)):
    db_parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")

    # Apply only provided fields
    for key, value in parent.dict(exclude_none=True).items():
        setattr(db_parent, key, value)

    db.commit()
    db.refresh(db_parent)  # Optional, if you want updated object returned
    return {"message": "Parent updated successfully", "data": db_parent}

def generate_parent_id(db: Session):
    last = db.query(Parent).order_by(Parent.id.desc()).first()
    if last:
        last_num = int(last.id[2:])  # Remove 'P' and convert to int
        new_id = f"PA{last_num + 1:04d}"
    else:
        new_id = "PA0001"
    return new_id