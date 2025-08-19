from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func, Text, DateTime,Enum
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.model.schema import UserCreate, UserUpdate
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint,UniqueConstraint
from sqlalchemy import Computed
from sqlalchemy import Column, Date
from core.database.databse import Base
import enum

class ClassSectionEnum(str, enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

class StudentClassAllocation(Base):
    __tablename__ = "studentclassallocation"
    id = Column(String(50), primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("student.id", ondelete="RESTRICT"), primary_key=True, index=True)
    student_class = Column(Integer, nullable=False)
    class_section = Column(String(50), nullable=False)
    reason = Column(String(50), nullable=False)

    student = relationship("Student", backref="student class allocation")

    __table_args__ = (
        CheckConstraint("student_class BETWEEN 1 AND 12", name="Student calss out or range"),
        CheckConstraint("class_section IN ('A','B','C','D')", name="class_section_out_of_range"),
        UniqueConstraint('student_id', name='uq_student_class_section'),)

class ClassTeacherAllocation(Base):
    __tablename__ = "classteacherallocation"
    id = Column(String(50), primary_key=True, index=True)
    teacher_id = Column(String(50), ForeignKey("teacher.id", ondelete="RESTRICT"), primary_key=True, index=True)
    teacher_class = Column(Integer, CheckConstraint("teacher_class BETWEEN 1 AND 12"), nullable=False)
    class_section = Column(Enum(ClassSectionEnum), nullable=False)
    reason = Column(String(50), nullable=False)

    teacher = relationship("Teacher", backref="classteacherallocation")

