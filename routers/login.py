from fastapi import APIRouter, Depends, HTTPException
from core.model.schema import LoginRequest
from core.database.databse import get_db
from sqlalchemy.orm import Session
from core.database.databsetable.tables_users import UserPasswordNew
from core.security.hashing import hash_password, verify_password 
from core.model.schema import PasswordChangeRequest

router = APIRouter(prefix="/login", tags=["login"])

@router.post("/")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserPasswordNew).filter(UserPasswordNew.id == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": data.username, "role": user.role}

@router.post("/change-password")
def change_password(req: PasswordChangeRequest, db: Session = Depends(get_db)):
    user = db.query(UserPasswordNew).filter(UserPasswordNew.id == req.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(req.old_password, user.password):
        raise HTTPException(status_code=401, detail="Old password incorrect")

    user.password = hash_password(req.new_password)
    db.commit()
    return {"message": "Password updated successfully"}