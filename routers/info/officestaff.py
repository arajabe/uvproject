from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import OfficeStaffCreate, OfficeStaffUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_users import OfficeStaff
from sqlalchemy.exc import SQLAlchemyError
from core.database.databsetable.tables_users import UserPassword
from core.model.schema import Password
from core.security.hashing import hash_password, verify_password 


router = APIRouter(prefix="/officestaff", tags=["users"])

@router.post("/")
def create_officestaff(office: OfficeStaffCreate, db: Session = Depends(get_db)):

    new_id = generate_officestaff_id(db)
    db_office= OfficeStaff(**office.dict(),id = new_id, reason = "new entry")
    db.add(db_office)
    try:
        db.commit()
        db.refresh(db_office)
        # 🔑 also create password record
        default_pw = "welcome123"  # <-- or student.dateofbirth, or ask in UI
        hashed_pw = hash_password(default_pw)
        db_userpass = UserPassword(id=db_office.id, role=office.role, password=hashed_pw)
        db.add(db_userpass)
        db.commit()
        return {"status": "created", "office staff" : db_office.id}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.delete("/{officestaff_id}")
def delete_officestaff(officestaff_id: str, db: Session = Depends(get_db)):
    officestaff = db.query(OfficeStaff).filter(OfficeStaff.id == officestaff_id).first()
    if not officestaff:
        raise HTTPException(404, "Office staff not found")
    db.delete(officestaff)
    try :
        db.commit()
        return {"status": "deleted", "office staff id": officestaff_id}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.patch("/{officestaff_id}")
def update_officestaff(officestaff_id: str, office_update: OfficeStaffUpdate, db: Session = Depends(get_db)):
    db_office = db.query(OfficeStaff).filter(OfficeStaff.id == officestaff_id).first()
    if not db_office:
        raise HTTPException(status_code=404, detail="office staff not found")

    # Apply only provided fields
    for key, value in office_update.dict(exclude_none=True).items():
        setattr(db_office, key, value)

    try:
        db.commit()
        db.refresh(db_office)
        return {"message": "office staff updated successfully", "updated office staff": db_office}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

def generate_officestaff_id(db: Session):
    last = db.query(OfficeStaff).order_by(OfficeStaff.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  
        new_id = f"OFF{last_num + 1:04d}"
    else:
        new_id = "OFF0001"
    return new_id