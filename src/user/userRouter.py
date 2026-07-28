from fastapi import APIRouter, Depends, status, Request
from src.user.userDtos import UserSchema, UserResponseSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user import userController
from src.utils.db import get_db


user_routes = APIRouter(prefix="/user")


@user_routes.post("/register",response_model=UserResponseSchema, status_code= status.HTTP_201_CREATED)
def register(body:UserSchema, db= Depends(get_db)):
    return userController.register(body,db)

@user_routes.post("/login", status_code=status.HTTP_200_OK)
def login(body:LoginSchema, db=Depends(get_db)):
    return userController.login_user(body, db)

@user_routes.get("/is_auth",response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def is_auth(request:Request, db=Depends(get_db)):
    return userController.is_auth(request, db)