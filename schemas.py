from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreateSchema(BaseModel):
    userName: str
    userEmail: EmailStr
    mobileNumber: str
    password: str

class UserResponseSchema(BaseModel):
    userId: str
    userName: str
    userEmail: EmailStr
    mobileNumber: str

class NoteCreateSchema(BaseModel):
    noteTitle: str
    noteContent: str

class NoteResponseSchema(BaseModel):
    noteId: str
    noteTitle: str
    noteContent: str
    createdOn: str
    lastUpdate: str
