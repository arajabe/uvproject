from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import ParentCreate, ParentUpdate
from core.db.db import get_db, Parent


router = APIRouter(prefix="/parent", tags=["parent"])

@router.post("/")
def create_parent(parent: ParentCreate, db: Session = Depends(get_db)):
    
    db_parent = Parent(name=parent.name, email=parent.email)
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    print("user request post")
    return {"status": "created", "parent": {"id": db_parent.id, "name": db_parent.name}}

@router.delete("/{parent_id}")
def delete_parent(parent_id: int, db: Session = Depends(get_db)):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(404, "Parent not found")
    db.delete(parent)
    db.commit()
    return {"status": "deleted", "id": parent_id}

@router.put("/{parent_id}")
def update_user(parent_id: int, parent: ParentUpdate, db: Session = Depends(get_db)):
    db_parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not db_parent:
        raise HTTPException(404, "parent not found")
    if parent.name: db_parent.name = parent.name
    if parent.email: db_parent.email = parent.email
    db.commit()
    return {"status": "updated", "id": db_parent.id}