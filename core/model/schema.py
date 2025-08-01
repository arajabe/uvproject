from typing import TypedDict, List
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