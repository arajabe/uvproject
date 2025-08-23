from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import UserCreate, UserUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_users import User
from sqlalchemy.exc import SQLAlchemyError
from core.database.databsetable.tables_users import UserPassword
from core.model.schema import Password
from core.security.hashing import hash_password, verify_password 


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    print("create_user(user: UserCreate, db: Session = Depends(get_db))")
    new_id = generate_user_id(db)
    db_user = User(name=user.name, email=user.email, fathername = user.fathername,
                         mothername = user.mothername, dateofbirth = user.dateofbirth, 
                         address =user.address, city = user.city, pincode = user.pincode, 
                         contactnumber = user.contactnumber, aadhar = user.aadhar, id = new_id, reason = user.reason)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user) 
         # 🔑 also create password record
        default_pw = "welcome123"  # <-- or student.dateofbirth, or ask in UI
        hashed_pw = hash_password(default_pw)
        db_userpass = UserPassword(id=db_user.id, role='parent', password=hashed_pw)
        db.add(db_userpass)
        db.commit() 
        return {"status": "user created", "user": db_user.id}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    try:
        db.commit()
        return {"status": "deleted", "id": user_id}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

@router.put("/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "reason":
            continue  # skip reason for DB update
        setattr(db_user, field, value)
    try:
        db.commit()
        db.refresh(db_user)
        return {"status": "user updated", "updated_fields": db_user}
    except SQLAlchemyError as e:
        db.rollback()
    # Return the SQL error details
        response =  str(e.__cause__ or e)
        return {"status": response}

def generate_user_id(db: Session):
    last = db.query(User).order_by(User.id.desc()).first()
    if last:
        last_num = int(last.id[3:])  
        new_id = f"USR{last_num + 1:04d}"
    else:
        new_id = "USR0001"
    return new_id