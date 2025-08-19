from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.model.schema import BulkOfficeStaff
from core.database.databse import get_db
from sqlalchemy.exc import SQLAlchemyError
from core.database.databsetable.tables_users import OfficeStaff


router = APIRouter(prefix="/office_staff", tags=["bulk_office_staff"])
    
@router.post("/upload")
def bulk_office_staff( bulk_data : BulkOfficeStaff, db: Session = Depends(get_db)):

    saved_records = []
    errors = []
    
  
    for record in bulk_data.records:
            
            new_id = generate_officestaff_id(db)
            
            db_office_staff = OfficeStaff(**record.dict(), id=new_id ,reason = "New Entry")
            db.add(db_office_staff)

            try:
                 db.commit()
                 db.refresh(db_office_staff)
                 saved_records.append({"office id": db_office_staff.id, "office staff name": db_office_staff.name})
            except SQLAlchemyError as e:
                db.rollback()
                errors.append({"office staff": record.name, "error": str(e.__cause__ or e)})            
            # saved_records.append(record) 
    return {"reply": {"status": "completed", "errors" : errors if errors else "no error on given data", "saved records" : saved_records}}
 
def generate_officestaff_id(db: Session):
    last = db.query(OfficeStaff).order_by(OfficeStaff.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  
        new_id = f"OFF{last_num + 1:04d}"
    else:
        new_id = "OFF0001"
    return new_id