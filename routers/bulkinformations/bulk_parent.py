from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.model.schema import BulkParent
from core.database.databse import get_db
from sqlalchemy.exc import SQLAlchemyError
from core.database.databsetable.tables_users import Parent


router = APIRouter(prefix="/parent", tags=["bulk_parent"])
    
@router.post("/upload")
def bulk_parent( bulk_data : BulkParent, db: Session = Depends(get_db)):

    saved_records = []
    errors = []
    
  
    for record in bulk_data.records:
            
            new_id = generate_parent_id(db)
            
            db_parent = Parent(**record.dict(), id=new_id , role = "parent", reason = "New Entry")
            db.add(db_parent)

            try:
                 db.commit()
                 db.refresh(db_parent)
                 saved_records.append({"parent_id": db_parent.id, "parent_name": db_parent.fathername})
            except SQLAlchemyError as e:
                db.rollback()
                errors.append({"parent": f"{record.fathername} record not created", "error": str(e.__cause__ or e)})            
            # saved_records.append(record) 
    return {"reply": {"status": "completed", "errors" : errors if errors else "no error on given data", "saved records" : saved_records}}
 
def generate_parent_id(db: Session):
    last = db.query(Parent).order_by(Parent.id.desc()).first()
    if last:
        last_num = int(last.id[2:])  # Remove 'P' and convert to int
        new_id = f"PA{last_num + 1:04d}"
    else:
        new_id = "PA0001"
    return new_id