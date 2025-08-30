from typing import TypedDict, List, Optional,Annotated
import json
from pydantic import BaseModel, EmailStr,constr, StringConstraints, Field

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

class PerformanceState(TypedDict):
    messages: List
    intent: str
    params: dict
    response : json
    response_pd : str
    role: str
    performance_request : str
    exam : str
    

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


class StudentCreate(BaseModel):
    parentid: str
    name: str
    dateofbirth: str
    email: EmailStr
    aadhar: AadharStr
    

class StudentUpdate(BaseModel):
    studentid : str
    name : Optional[str] = None 
    parentid: Optional[str] = None
    dateofbirth: Optional[str] = None 
    parentrelation : Optional[str] = None
    email: Optional[EmailStr] = None
    aadhar : Optional[AadharStr] = None
    reason : str

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

class ParentCreate(BaseModel):
    fathername: str
    mothername: str
    parentrelation : str
    address: str
    city: str
    pincode: PincodeStr # 6-digit pincode
    contactnumber: ContactNumberStr  # Valid 10-digit Indian number
    alternate_contactnumber: ContactNumberStr  # Valid 10-digit Indian number
    email: EmailStr
    aadhar: AadharStr    
    occupation : str 

class ParentUpdate(BaseModel):
    parentid : str
    fathername: Optional[str] = None
    mothername: Optional[str] = None
    parentrelation : Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode : Optional[PincodeStr] = None
    contactnumber : Optional[ContactNumberStr] = None
    alternate_contactnumber : Optional[ContactNumberStr] = None
    email: Optional[EmailStr] = None
    aadhar : Optional[AadharStr] = None       
    occupation : Optional[str] = None
    reason : str 


class MarkCreate(BaseModel):
    student_id: str 
    term : int 
    language_1 : int
    language_2 : int 
    maths : int 
    science : int 
    social_science : int

class MarkUpdate(BaseModel):
    student_id: Optional[str] = None
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
    abscent : str

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

class Password(BaseModel):
    id: str
    password : str
    role : str

class StudentClassAllocationCreate(BaseModel):
    student_id : str
    student_class : int
    class_section : str

class StudentClassAllocationUpdate(BaseModel):
    student_class_allocation_id : str
    student_id : Optional[str] = None
    student_class : Optional[int] = None
    class_section : Optional[str] = None
    reason : str

class ClassTeacherAllocationCreate(BaseModel):
    teacher_id : str
    teacher_class : int
    class_section : str

class ClassTeacherAllocationUpdate(BaseModel):
    teacher_id : Optional[str]
    teacher_class : Optional[int]
    class_section : Optional[str]
    class_teacher_allocation_id : str
    reason : str

class AuditTableSchema(BaseModel):
    status : str
    table_field : str
    old_value : str
    new_value : str

class BulkSubjectTermSplit(BaseModel):
    records: List[SubjectTermSplitCreate]

class BulkAssignement(BaseModel):
    records: List[AssignementCreate]

class BulkTermMark(BaseModel):
    records: List[MarkCreate]

class BulkParent(BaseModel):
    records : List[ParentCreate]
    
class BulkStudent(BaseModel):
    records : List[StudentCreate]
class BulkTeacher(BaseModel):
    records : List[TeacherCreate]

class BulkOfficeStaff(BaseModel):
    records : List[OfficeStaffCreate]
class BulkStudentClassAllocation(BaseModel):
    records : List[StudentClassAllocationCreate]
class BulkClassTeacherAllocation(BaseModel):
    records : List[ClassTeacherAllocationCreate]

class PasswordChangeRequest(BaseModel):
    username: str
    old_password: str
    new_password: str

