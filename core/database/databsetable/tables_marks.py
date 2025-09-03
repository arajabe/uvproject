from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func, Text, DateTime
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint,UniqueConstraint,ForeignKeyConstraint
from sqlalchemy import Computed
from sqlalchemy import Column, Date
from core.database.databse import Base



class Mark(Base):
    __tablename__ = "termmark"          
    id = Column(String(50), primary_key=True, index=True)
    student_id = Column(String(50), ForeignKey("studentclassallocation.student_id", ondelete="RESTRICT"), nullable=False)
    term = Column(Integer, nullable=False, index=True)
    language_1 = Column(Integer, nullable=False, index=True)
    language_2 = Column(Integer, nullable=False, index=True)
    maths = Column(Integer, nullable=False, index=True)
    science = Column(Integer, nullable=False, index=True)
    social_science = Column(Integer, nullable=False, index=True)       
    total = Column(Integer, Computed("language_1 + language_2 + maths + science + social_science"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    studentclassallocation = relationship("StudentClassAllocation", backref="Student_Class_Allocation_marks")

    __table_args__ = (
        CheckConstraint('term >= 1 AND term <= 3', name='mark term is not in range'),
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
    student_id = Column(String(50), ForeignKey("studentclassallocation.student_id", ondelete="RESTRICT"), nullable=False)
    term = Column(Integer, nullable=False, index=True)
    period = Column(Integer, nullable=False, index=True)
    language_1 = Column(Integer, nullable=False, index=True)
    language_2 = Column(Integer, nullable=False, index=True)
    maths = Column(Integer, nullable=False, index=True)
    science = Column(Integer, nullable=False, index=True)
    social_science = Column(Integer, nullable=False, index=True)
    total = Column(Integer, Computed("language_1 + language_2 + maths + science + social_science"), nullable=False)  
    timestamp = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('term >= 1 AND term <= 3', name='Assignemnt term is not in range'),
        CheckConstraint('period >= 1 AND period <= 10', name='assignement period is not in range'),
        CheckConstraint('language_1 BETWEEN 0 AND 10', name='language_1 assignement mark is not in range'),
        CheckConstraint('language_2 BETWEEN 0 AND 10', name='language 2 assignement mark is not in range'),
        CheckConstraint('maths BETWEEN 0 AND 10', name='maths assignement mark is not in range'),
        CheckConstraint('science BETWEEN 0 AND 10', name='science assignement mark is not in range'),
        CheckConstraint('social_science BETWEEN 0 AND 10', name='social assignement mark is not in range'),
        UniqueConstraint('student_id', 'term', 'period', name='Duplicate')
    )

    studentclassallocation = relationship("StudentClassAllocation", backref="marks_assignement")


class SubjectTermSplit(Base):
    __tablename__ = "subject_term_split"          
    id = Column(String(50), primary_key=True, index=True)
    student_id = Column(String(50),ForeignKey("studentclassallocation.student_id", ondelete="RESTRICT"), nullable=False)
    term = Column(Integer, nullable=False, index=True)
    subject = Column(String(50), nullable=False)
    mark_section_A = Column(Integer, nullable=False, index=True)
    mark_section_B = Column(Integer, nullable=False, index=True)
    mark_section_C = Column(Integer, nullable=False, index=True)
    mark_section_D = Column(Integer, nullable=False, index=True)
    total = Column(Integer, Computed("mark_section_A + mark_section_B + mark_section_C + mark_section_D"), nullable=False)     
    abscent = Column(String(50), nullable=False, index=True)

    timestamp = Column(DateTime, default=datetime.utcnow)
    
    studentclassallocation = relationship("StudentClassAllocation", backref="Student_Class_Allocation_subject_term_split")

    __table_args__ = (
        CheckConstraint('term >= 1 AND term <= 3', name='subject term is not in range'),
        CheckConstraint('mark_section_A >= 0 AND mark_section_A <= 20', name='mark_range_section_A'),
        CheckConstraint('mark_section_B >= 0 AND mark_section_B <= 20', name='mark_range_section_B'),
        CheckConstraint('mark_section_C >= 0 AND mark_section_C <= 20', name='mark_range_section_C'),
        CheckConstraint('mark_section_D >= 0 AND mark_section_D <= 20', name='mark_range_section_D'),
        CheckConstraint("abscent IN ('yes', 'no')", name="abscent_tem_mark_split"),
        CheckConstraint("subject IN ('language_1', 'language_2', 'maths', 'science', 'social_science')", name="subject_tem_mark_split"),
        CheckConstraint("(abscent = 'no') OR " "(abscent = 'yes' AND mark_section_A = 0 AND mark_section_B = 0 "
                            "AND mark_section_C = 0 AND mark_section_D = 0)", name="check_abscent_term_split_mark"),
        CheckConstraint("total <= 80", name= 'subject_total'),
        UniqueConstraint('student_id', 'term', 'subject', name='uq_student_term_period_assignement'),
        
    )
