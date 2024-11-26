from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from database import db
from schemas import UserCreateSchema, UserResponseSchema, NoteCreateSchema, NoteResponseSchema
from auth import createAccessToken, decodeToken, verifyPassword
from crud import createUser, getUserByEmail, createNoteForUser, getNotesByUser
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register", response_model=UserResponseSchema)
async def register(user: UserCreateSchema):
    existingUser = await getUserByEmail(user.userEmail)
    if existingUser:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return await createUser(user.dict())

@app.post("/login")
async def login(user: UserCreateSchema):
    dbUser = await getUserByEmail(user.userEmail)
    if not dbUser or not verifyPassword(user.password, dbUser["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = createAccessToken(data={"sub": dbUser["userEmail"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/notes", response_model=NoteResponseSchema)
async def createNote(note: NoteCreateSchema, token: str = Depends(oauth2Scheme)):
    payload = decodeToken(token)
    userEmail = payload.get("sub")
    user = await getUserByEmail(userEmail)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return await createNoteForUser(note.dict(), user["_id"])

@app.get("/notes", response_model=list[NoteResponseSchema])
async def getNotes(token: str = Depends(oauth2Scheme)):
    payload = decodeToken(token)
    userEmail = payload.get("sub")
    user = await getUserByEmail(userEmail)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return await getNotesByUser(user["_id"])
