from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database.databse import get_db
from core.database.databsetable.tables_users import UserPassword
from core.model.schema import Password
from core.security.hashing import hash_password, verify_password 

router = APIRouter(prefix="/password", tags=["password"])

@router.post("/create")
def create_userpass(req: Password, db: Session = Depends(get_db)):
    hashed_pw = hash_password(req.password)
    new_user = UserPassword(id=req.id, role=req.role, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "role": new_user.role}