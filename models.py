from pydantic import BaseModel, EmailStr
from uuid import uuid4
from datetime import datetime

class UserModel(BaseModel):
    userId: str = str(uuid4())
    userName: str
    userEmail: EmailStr
    mobileNumber: str
    password: str
    lastUpdate: datetime = datetime.now()
    createdOn: datetime = datetime.now()

class NoteModel(BaseModel):
    noteId: str = str(uuid4())
    noteTitle: str
    noteContent: str
    lastUpdate: datetime = datetime.now()
    createdOn: datetime = datetime.now()
