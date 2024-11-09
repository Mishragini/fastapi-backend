import uvicorn 
import bcrypt
import jwt as PyJWT
import os

from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import FastAPI,Depends,HTTPException,status
from db.database import get_db
from db.models import User
from sqlalchemy.orm import Session
from api.endpoints.user import user_router
from api.endpoints.admin import admin_router
from role import Role
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Role

class UserSignin(BaseModel):
    email:str
    password:str


load_dotenv()
SECRET_KEY=os.getenv('SECRET_KEY')
ALGORITHM=os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES','30'))



app=FastAPI()

@app.get("/")
def health():
    return {"msg":"Server looks good"}

@app.post("/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
            )

    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'), bcrypt.gensalt()
    ).decode('utf-8')

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": str(new_user.id),
        "message": "Signed up successfully!"
    }


@app.post("/login")
def login_user(user:UserSignin,db:Session= Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exists")
        
    passworMatched = bcrypt.checkpw(user.password.encode('utf-8'),db_user.password_hash.encode('utf-8'))   
    if not passworMatched:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token= PyJWT.encode(
        {"sub":db_user.username,"exp":datetime.utcnow()+access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "message":"Logged in successfully!"
    }

app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(user_router, prefix="/user", tags=["user"])

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000, reload=False)