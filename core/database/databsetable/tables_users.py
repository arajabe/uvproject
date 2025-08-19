from sqlalchemy import create_engine, String, TIMESTAMP, func
from sqlalchemy import Column,ForeignKey
from core.database.databse import Base
from sqlalchemy.orm import relationship


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
    parentid = Column(String(50),nullable= False)
    role = Column(String(15), nullable = False)
    parentrelation = Column(String(15), nullable = False)

class Teacher(Base):
    __tablename__ = "teacher"
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
    graduatedegree = Column(String(50), nullable=False) 
    subject = Column(String(50), nullable=False)
