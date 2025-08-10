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

DATABASE_URL = "mysql+pymysql://root:Nannilam123@127.0.0.1/testdb"
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    fathername = Column(String(50), nullable=False)
    mothername = Column(String(50), nullable=False)
    dateofbirth = Column(String(50), nullable = False)
    address = Column(String(200), nullable=False)
    city = Column(String(50), nullable=False)
    pincode = Column(String(6), nullable=False)
    contactnumber = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False)
    aadhar = Column(String(17), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True)
    role = Column(String(24))
    user_msg = Column(Text)
    bot_reply = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Student(Base):
    __tablename__ = "student"
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    fathername = Column(String(50), nullable=False)
    mothername = Column(String(50), nullable=False)
    dateofbirth = Column(String(50), nullable = False)
    address = Column(String(200), nullable=False)
    city = Column(String(50), nullable=False)
    pincode = Column(String(6), nullable=False)
    contactnumber = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False)
    aadhar = Column(String(17), nullable=False)
    reason = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    parentid = Column(String(50), nullable= False)
    role = Column(String(15), nullable = False)
    parentrelation = Column(String(15), nullable = False)

class Teacher(Base):
    __tablename__ = "Teacher"
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    fathername = Column(String(50), nullable=False)
    mothername = Column(String(50), nullable=False)
    dateofbirth = Column(String(50), nullable = False)
    address = Column(String(200), nullable=False)
    city = Column(String(50), nullable=False)
    pincode = Column(String(6), nullable=False)
    contactnumber = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False)
    aadhar = Column(String(17), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    reason = Column(String(50), nullable=False)
    graduatedegree = Column(String(50), nullable=False) 
    subject = Column(String(50), nullable=False)
    role = Column(String(15), nullable= False)


class Parent(Base):
    __tablename__ = "parent"
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    fathername = Column(String(50), nullable=False)
    mothername = Column(String(50), nullable=False)
    dateofbirth = Column(String(50), nullable = False)
    address = Column(String(200), nullable=False)
    city = Column(String(50), nullable=False)
    pincode = Column(String(6), nullable=False)
    contactnumber = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False)
    aadhar = Column(String(17), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    reason = Column(String(50), nullable=False)
    fatheroccupation = Column(String(50), nullable=False)
    motheroccupation = Column(String(50), nullable=False)
    role = Column(String(15), nullable = False)

class OfficeStaff(Base):
    __tablename__ = "officestaff"
    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    fathername = Column(String(50), nullable=False)
    mothername = Column(String(50), nullable=False)
    dateofbirth = Column(String(50), nullable = False)
    address = Column(String(200), nullable=False)
    city = Column(String(50), nullable=False)
    pincode = Column(String(6), nullable=False)
    contactnumber = Column(String(10), nullable=False)
    email = Column(String(50), nullable=False)
    aadhar = Column(String(17), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    reason = Column(String(15), nullable = False)
    role = Column(String(15), nullable = False)

class Mark(Base):
    __tablename__ = "termmark"  
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("student.id"), nullable=False)
    term = Column(Integer, nullable=False, index=True)
    language_1_status = Column(String(5), Computed("CASE WHEN language_1 >= 35 THEN 'pass' ELSE 'fail' END"), nullable=False)
    language_1 = Column(Integer, nullable=False, index=True)
    language_2_status = Column(String(5), Computed("CASE WHEN language_2 >= 35 THEN 'pass' ELSE 'fail' END"), nullable=False)
    language_2 = Column(Integer, nullable=False, index=True)
    maths_status = Column(String(5), Computed("CASE WHEN maths >= 35 THEN 'pass' ELSE 'fail' END"), nullable=False)
    maths = Column(Integer, nullable=False, index=True)
    science_status = Column(String(5), Computed("CASE WHEN science >= 35 THEN 'pass' ELSE 'fail' END"), nullable=False)
    science = Column(Integer, nullable=False, index=True)
    social_science_status = Column(String(5), Computed("CASE WHEN social_science >= 35 THEN 'pass' ELSE 'fail' END"), nullable=False)
    social_science = Column(Integer, nullable=False, index=True)       
    total = Column(Integer, Computed("language_1 + language_2 + maths + science + social_science"), nullable=False)
    overall_status = Column(
    String(5),
    Computed(
        "CASE WHEN (language_1 >= 35 AND language_2 >= 35 AND maths >= 35 AND science >= 35 AND social_science >= 35) THEN 'pass' ELSE 'fail' END",
        persisted=True
    ),
    nullable=False,)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", backref="marks")

    __table_args__ = (
        CheckConstraint('language_1 >= 0 AND language_1 <= 100', name='lang1_range'),
        CheckConstraint('language_2 >= 0 AND language_2 <= 100', name='lang2_range'),
        CheckConstraint('maths >= 0 AND language_2 <= 100', name='maths_range'),
        CheckConstraint('science >= 0 AND language_2 <= 100', name='sscience_range'),
        CheckConstraint('social_science >= 0 AND language_2 <= 100', name='social_science_range'),
        CheckConstraint('total >= 0 AND total <= 500', name='total_range'),
        UniqueConstraint('student_id', 'term', name='uq_student_term')
    )

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()