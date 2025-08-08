from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import UserCreate, UserUpdate
from core.db.db import get_db, User


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print("create_user(user: UserCreate, db: Session = Depends(get_db))")
    new_id = generate_user_id(db)
    db_user = User(name=user.name, email=user.email, fathername = user.fathername,
                         mothername = user.mothername, dateofbirth = user.dateofbirth, 
                         address =user.address, city = user.city, pincode = user.pincode, 
                         contactnumber = user.contactnumber, aadhar = user.aadhar, id = new_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print("user request post")
    return {"status": "created", "user": {"id": db_user.id, "name": db_user.name}}

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()
    return {"status": "deleted", "id": user_id}

@router.put("/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(404, "User not found")
    if user.name: db_user.name = user.name
    if user.email: db_user.email = user.email
    db.commit()
    return {"status": "updated", "id": db_user.id}

def generate_user_id(db: Session):
    last = db.query(User).order_by(User.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  
        new_id = f"USR{last_num + 1:04d}"
    else:
        new_id = "USR0001"
    return new_id