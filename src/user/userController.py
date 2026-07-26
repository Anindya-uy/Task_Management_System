from fastapi import HTTPException, status
from src.user.userDtos import UserSchema
from sqlalchemy.orm import Session
from src.user.userModels import UserModel
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


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