from database import db
from models import UserModel, NoteModel
from auth import hashPassword, verifyPassword
from bson import ObjectId

async def createUser(userData: dict):
    userData['password'] = hashPassword(userData['password'])
    user = UserModel(**userData)
    await db.users.insert_one(user.dict())
    return user

async def getUserByEmail(email: str):
    return await db.users.find_one({"userEmail": email})

async def createNoteForUser(noteData: dict, userId: str):
    noteData['userId'] = userId
    note = NoteModel(**noteData)
    await db.notes.insert_one(note.dict())
    return note

async def getNotesByUser(userId: str):
    return await db.notes.find({"userId": userId}).to_list(100)
