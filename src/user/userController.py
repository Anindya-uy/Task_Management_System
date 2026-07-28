from fastapi import HTTPException, status
from src.user.userDtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.userModels import UserModel
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime,timedelta
import jwt


password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def register(body:UserSchema, db:Session):
    #print(body)
    
    # User Validations
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400, detail="username already exists..")

    # Email Validations
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(400, detail="Email already exist..")

    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        username = body.username,
        hased_password = hash_password,
        email = body.email,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    
    return new_user

def login_user(body:LoginSchema, db:Session):
    #print(body)
    
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You entered wrong Username!")

    if not verify_password(body.password, user.hased_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You entered wrong Password!")

    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    time = exp_time.timestamp()
    token = jwt.encode({"_id":user.id, "exp_time":time},settings.SECRET_KEY, settings.ALGORITHM)
    
    return {"token":token}