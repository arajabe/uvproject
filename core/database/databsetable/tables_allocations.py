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


class StudentClass(Base):
    __tablename__ = "studentclass"
    id = Column(String(50), primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("student.id"), primary_key=True, index=True)
    student_name = Column(String(50), nullable=False)
    student_class = Column(String(10), nullable = False)
    class_section = Column(String(10), nullable = False)

    student = relationship("Student", backref="student_class")

    UniqueConstraint('student_id', 'student_class', class_section, name='uq_student_class')

class ClassTeacher(Base):
    __tablename__ = "classteacher"
    id = Column(String(50), primary_key=True, index=True)
    teacher_id = Column(String(50),primary_key=True, index=True)
    teaher_name = Column(String(50), nullable=False)
    teacher_class = Column(String(10), nullable = False)
    class_section = Column(String(10), nullable = False)

    teacher = relationship("teacher", backref="teacher_class")
