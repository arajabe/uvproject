from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func, Text, DateTime
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint,UniqueConstraint
from sqlalchemy import Computed
from sqlalchemy import Column, Date
from core.database.databse import Base


class Mark(Base):
    __tablename__ = "termmark"          
    id = Column(String(50), primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("student.id"), nullable=False)
    student_name = Column(String(50), index=True)
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
        CheckConstraint('language_1 >= 0 AND language_1 <= 100', name='language_1 mark is not in range'),
        CheckConstraint('language_2 >= 0 AND language_2 <= 100', name='language_2 mark is not in range'),
        CheckConstraint('maths >= 0 AND maths <= 100', name='maths mark is not in range'),
        CheckConstraint('science >= 0 AND science <= 100', name='science mark is not in range'),
        CheckConstraint('social_science >= 0 AND social_science <= 100', name='social_science mark is not in range'),
        CheckConstraint('total >= 0 AND total <= 500', name='total_range'),
        UniqueConstraint('student_id', 'term', name='either student_id or term is duplicate')
    )


class Assignement(Base):
    __tablename__ = "assignement"          
    id = Column(String(50), primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("student.id"), nullable=False)
    student_name = Column(String(50), index=True)
    term = Column(Integer, nullable=False, index=True)
    period = Column(Integer, nullable=False, index=True)
    language_1 = Column(Integer, nullable=False, index=True)
    language_2 = Column(Integer, nullable=False, index=True)
    maths = Column(Integer, nullable=False, index=True)
    science = Column(Integer, nullable=False, index=True)
    social_science = Column(Integer, nullable=False, index=True)       

    timestamp = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", backref="marks_assignement")

    __table_args__ = (
        CheckConstraint('language_1 >= 0 AND language_1 <= 10', name='language_1 assignement mark is not in range'),
        CheckConstraint('language_2 >= 0 AND language_2 <= 10', name='language 2 assignement mark is not in range'),
        CheckConstraint('maths >= 0 AND maths <= 10', name='maths assignement mark is not in range'),
        CheckConstraint('science >= 0 AND science <= 10', name='sscience assignement mark is not in range '),
        CheckConstraint('social_science >= 0 AND social_science <= 10', name='social assignement mark is not in range'),
        UniqueConstraint('student_id', 'term', 'period', name='Duplicate')
    )


class SubjectTermSplit(Base):
    __tablename__ = "subject_term_split"          
    id = Column(String(50), primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("student.id"), nullable=False)
    student_name = Column(String(50), index=True)
    term = Column(Integer, nullable=False, index=True)
    subject = Column(String(50), nullable=False)
    mark_section_A = Column(Integer, nullable=False, index=True)
    mark_section_B = Column(Integer, nullable=False, index=True)
    mark_section_C = Column(Integer, nullable=False, index=True)
    mark_section_D = Column(Integer, nullable=False, index=True)
    subject_total = Column(Integer, Computed("mark_section_A + mark_section_B + mark_section_C + mark_section_D"), nullable=False)     

    timestamp = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", backref="subject_mark_term_split")

    __table_args__ = (
        CheckConstraint('mark_section_A >= 0 AND mark_section_A <= 20', name='mark_range_section_A'),
        CheckConstraint('mark_section_B >= 0 AND mark_section_B <= 20', name='mark_range_section_B'),
        CheckConstraint('mark_section_C >= 0 AND mark_section_C <= 20', name='mark_range_section_C'),
        CheckConstraint('mark_section_D >= 0 AND mark_section_D <= 20', name='mark_range_section_D'),
        CheckConstraint("subject_total <= 80", name= 'subject_total'),
        UniqueConstraint('student_id', 'term', 'subject', name='uq_student_term_period_assignement')
    )
