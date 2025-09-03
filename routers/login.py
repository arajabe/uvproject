from fastapi import APIRouter, Depends, HTTPException
from core.model.schema import LoginRequest
from core.database.databse import get_db
from sqlalchemy.orm import Session
from core.database.databsetable.tables_users import UserPasswordNew
from core.security.hashing import hash_password, verify_password 
from core.model.schema import PasswordChangeRequest
from core.utils.audit_events import set_audit_user
from routers.logging_config import setup_logger
import logging
from datetime import datetime, timedelta


router = APIRouter(prefix="/login", tags=["login"])

logger = setup_logger("backend")   # use same backend logger

# Get the same logger initialized in main
#logger = logging.getLogger("backend")



@router.post("/")
def login(data: LoginRequest, db: Session = Depends(get_db)):
   

    # Check if any user is already logged in
    user = db.query(UserPasswordNew).filter(UserPasswordNew.id == data.username).first()

    if user.is_logged_in:
        logger.info(f"❌ Another user logging as '{data.username}'")
        raise HTTPException(status_code=403, detail=f"User '{user.id}' is already logged in")
    else:
        user = db.query(UserPasswordNew).filter(UserPasswordNew.id == data.username).first()
    # client_ip = request.client.host
        set_audit_user(data.username)
        if not user:
            logger.warning(f"❌ Failed login attempt for '{data.username}'")
            raise HTTPException(status_code=404, detail="User not found")

        elif not verify_password(data.password, user.password):
            logger.warning(f"❌ Failed login attempt for '{data.username}'")
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Mark user as logged in
    user.is_logged_in = True
    user.last_activity = datetime.utcnow()
    user.session_expiry = datetime.utcnow() + timedelta(minutes=1)  # auto-expire after 30m
    db.commit()
    logger.info(f"✅ User '{data.username}' logged in")
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

@router.post("/logout")
def logout(username: str, db: Session = Depends(get_db)):
    user = db.query(UserPasswordNew).filter(UserPasswordNew.id == username).first()
    if user:
        user.is_logged_in = False
        db.commit()
        logger.info(f"👋 User '{username}' logged out")
        return {"message": f"User '{username}' logged out"}
    raise HTTPException(status_code=404, detail="User not logged in")
