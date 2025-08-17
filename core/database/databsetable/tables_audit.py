from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import UserCreate, UserUpdate
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint,UniqueConstraint
from sqlalchemy import Computed
from sqlalchemy import Column, Date
from core.database.databse import Base


class AuditTable(Base):
    __tablename__ = "audittable"
    id = Column(String(50), primary_key=True, index=True)
    table_id = Column(String(50), primary_key=True, index=True)
    rason = Column(String(50), nullable=False)
