from typing import TypedDict, List, Optional,Annotated
import os, json, requests
from pydantic import BaseModel, EmailStr,constr, StringConstraints
import pandas
from datetime import date


ContactNumberStr = Annotated[str, StringConstraints(pattern=r'^\d{10}$')] # Valid 10-digit Indian number
PincodeStr = Annotated[str, StringConstraints(pattern=r'^\d{6}$')] # validate 6-digit pincode
AadharStr = Annotated[str, StringConstraints(pattern=r'^\d{12}$')] # valid 12-digit Aadhar

class ChatState(TypedDict):
    messages: List
    intent: str
    params: dict
    response : json
    response_pd : str

class UserCreate(BaseModel):
    name: str
    fathername: str
    mothername: str
    dateofbirth: str
    address: str
    city: str
    pincode: PincodeStr # 6-digit pincode
    contactnumber: ContactNumberStr  # Valid 10-digit Indian number
    email: EmailStr
    aadhar: AadharStr

class UserUpdate(BaseModel):
    name: Optional[str] = None
    fathername : Optional[str] = None
    mothername : Optional[str] = None
    dateofbirth : Optional[date] = None
    address : Optional[str] = None
    city : Optional[str] = None
    pincode : Optional[PincodeStr] = None
    contactnumber : Optional[ContactNumberStr] = None
    email: Optional[EmailStr] = None
    aadhar : Optional[AadharStr] = None

class StudentCreate(BaseModel):
    name: str
    fathername: str
    mothername: str
    dateofbirth: str
    address: str
    city: str
    pincode: PincodeStr # 6-digit pincode
    contactnumber: ContactNumberStr  # Valid 10-digit Indian number
    email: EmailStr
    aadhar: AadharStr

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    fathername : Optional[str] = None
    mothername : Optional[str] = None
    dateofbirth : Optional[str] = None
    address : Optional[str] = None
    city : Optional[str] = None
    pincode : Optional[PincodeStr] = None
    contactnumber : Optional[ContactNumberStr] = None
    email: Optional[EmailStr] = None
    aadhar : Optional[AadharStr] = None

class TeacherCreate(BaseModel):
    name: str
    fathername: str
    mothername: str
    dateofbirth: str
    address: str
    city: str
    pincode: PincodeStr # 6-digit pincode
    contactnumber: ContactNumberStr  # Valid 10-digit Indian number
    email: EmailStr
    aadhar: AadharStr


class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    fathername : Optional[str] = None
    mothername : Optional[str] = None
    dateofbirth : Optional[str] = None
    address : Optional[str] = None
    city : Optional[str] = None
    pincode : Optional[PincodeStr] = None
    contactnumber : Optional[ContactNumberStr] = None
    email: Optional[EmailStr] = None
    aadhar : Optional[AadharStr] = None

class ParentCreate(BaseModel):
    name: str
    fathername: str
    mothername: str
    dateofbirth: str
    address: str
    city: str
    pincode: PincodeStr # 6-digit pincode
    contactnumber: ContactNumberStr  # Valid 10-digit Indian number
    email: EmailStr
    aadhar: AadharStr

class ParentUpdate(BaseModel):
    name: Optional[str] = None
    fathername : Optional[str] = None
    mothername : Optional[str] = None
    dateofbirth : Optional[str] = None
    address : Optional[str] = None
    city : Optional[str] = None
    pincode : Optional[PincodeStr] = None
    contactnumber : Optional[ContactNumberStr] = None
    email: Optional[EmailStr] = None
    aadhar : Optional[AadharStr] = None

class MarkCreate(BaseModel):
    student_id: int | None = None
    term : int | None = None
    language_1 : int | None = None
    language_2 : int | None = None
    maths : int |None = None
    science : int | None = None
    social_science : int | None = None

class MarkUpdate(BaseModel):
    student_id: int = None
    term: int = None
    language_1: Optional[int] = None
    language_2: Optional[int] = None
    maths: Optional[int] = None
    science: Optional[int] = None
    social_science: Optional[int] = None

class MarkQueryParams(BaseModel):
    student_id: int
    subject: List[str]  # e.g. ["maths", "science"]
    term: List[int] 

class RequestPayload(BaseModel):
    params: MarkQueryParams

class LoginRequest(BaseModel):
    username: str
    password: str