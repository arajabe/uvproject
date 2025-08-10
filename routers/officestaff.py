from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import OfficeStaffCreate, OfficeStaffUpdate
from core.db.db import get_db, OfficeStaff


router = APIRouter(prefix="/officestaff", tags=["users"])

@router.post("/")
def create_officestaff(office: OfficeStaffCreate, db: Session = Depends(get_db)):

    new_id = generate_officestaff_id(db)
    db_office= office(name=office.name, email=office.email, fathername = office.fathername,
                         mothername = office.mothername, dateofbirth = office.dateofbirth, 
                         address =office.address, city = office.city, pincode = office.pincode, 
                         contactnumber = office.contactnumber, aadhar = office.aadhar, id = new_id, reason = office.reason,
                         role = office.role, graduatedegree = office.graduatedegree,  subject = office.subject)
    db.add(db_office)
    db.commit()
    db.refresh(db_office)

    return {"status": "created", "office staff": {"id": db_office.id, "name": db_office.name}}

@router.delete("/{officestaff_id}")
def delete_officestaff(officestaff_id: str, db: Session = Depends(get_db)):
    officestaff = db.query(OfficeStaff).filter(OfficeStaff.id == officestaff_id).first()
    if not officestaff:
        raise HTTPException(404, "Office staff not found")
    db.delete(officestaff)
    db.commit()
    return {"status": "deleted", "office staff id": officestaff_id}

@router.patch("/{officestaff_id}")
def update_officestaff(officestaff_id: str, office: OfficeStaffUpdate, db: Session = Depends(get_db)):
    db_office = db.query(OfficeStaff).filter(OfficeStaff.id == officestaff_id).first()
    if not db_office:
        raise HTTPException(status_code=404, detail="office staff not found")

    # Apply only provided fields
    for key, value in office.dict(exclude_none=True).items():
        setattr(db_office, key, value)

    db.commit()
    db.refresh(db_office)

    return {"message": "Teacher updated successfully", "data": db_office}

def generate_officestaff_id(db: Session):
    last = db.query(OfficeStaff).order_by(OfficeStaff.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  
        new_id = f"OFF{last_num + 1:04d}"
    else:
        new_id = "OFF0001"
    return new_id