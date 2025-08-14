from typing import TypedDict, List, Optional,Annotated
import os, json, requests
from pydantic import BaseModel, EmailStr,constr, StringConstraints, Field
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
    role: str
    radio_action_on_person: str

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
    reason : str

class UserUpdate(BaseModel):
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
    reason: str = Field(..., description="Reason for update (required)")

class UserDelete(BaseModel):
    id : str
    reason : str


class StudentCreate(UserCreate):
    parentid: str
    parentrelation : str


class StudentUpdate(UserUpdate):
    studentid : str
    parentid: Optional[str] = None
    parentrelation : Optional[str] = None

class TeacherCreate(UserCreate):
    graduatedegree : str    
    subject : str

class TeacherUpdate(UserUpdate):
    teacherid : str
    graduatedegree :Optional[str]  = None 
    subject : Optional[str] = None

class OfficeStaffCreate(UserCreate):
    graduatedegree : str    
    subject : str
    role : str

class OfficeStaffUpdate(UserUpdate):
    officestaffid : str
    graduatedegree :Optional[str]  = None 
    subject : Optional[str] = None
    role : str

class ParentCreate(UserCreate):
    fatheroccupation : str
    motheroccupation : str

class ParentUpdate(UserUpdate):
    parentid : str
    fatheroccupation : Optional[str] = None
    motheroccupation : Optional[str] = None

class MarkCreate(BaseModel):
    student_id: str 
    term : int 
    language_1 : int
    language_2 : int 
    maths : int 
    science : int 
    social_science : int

class MarkUpdate(BaseModel):
    student_id: Optional[int] = None
    term: Optional[int] = None
    language_1: Optional[int] = None
    language_2: Optional[int] = None
    maths: Optional[int] = None
    science: Optional[int] = None
    social_science: Optional[int] = None

class MarkDelete(BaseModel):
    student_id: str 
    term : int 

class AssignementUpdate(BaseModel):
    student_id : Optional[str] = None
    term : Optional[int] = None
    period : Optional[int] = None
    language_1 : Optional[int] = None
    language_2 : Optional[int] = None
    maths : Optional[int] = None
    science : Optional[int] = None
    social_science : Optional[int] = None

class AssignementCreate(BaseModel):
    student_id : str
    term : int
    period : int
    language_1 : int
    language_2 : int
    maths : int
    science : int
    social_science : int

class AssignementDelete(BaseModel):
    student_id : str
    term : int
    period : int

class SubjectTermSplitCreate(BaseModel):         
    student_id : str
    term : int
    subject : str
    mark_section_A : int
    mark_section_B : int
    mark_section_C : int
    mark_section_D : int

class SubjectTermSplitDelete(BaseModel):         
    student_id : str
    term : int
    subject : str

class MarkQueryParams(BaseModel):
    student_id: int
    subject: List[str]  # e.g. ["maths", "science"]
    term: List[int] 

class RequestPayload(BaseModel):
    params: MarkQueryParams

class LoginRequest(BaseModel):
    username: str
    password: str