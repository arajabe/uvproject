from typing import TypedDict, List, Optional
import os, json, requests
from pydantic import BaseModel, EmailStr

class ChatState(TypedDict):
    messages: List
    intent: str
    params: dict
    response : json

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class StudentCreate(BaseModel):
    name: str
    email: EmailStr

class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class TeacherCreate(BaseModel):
    name: str
    email: EmailStr

class TeacherUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class ParentCreate(BaseModel):
    name: str
    email: EmailStr

class ParentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

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