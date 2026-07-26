from fastapi import APIRouter, Depends, status
from src.user.userDtos import UserSchema, UserResponseSchema
from sqlalchemy.orm import Session
from src.user import userController
from src.utils.db import get_db


user_routes = APIRouter(prefix="/user")


@user_routes.post("/register",response_model=UserResponseSchema, status_code= status.HTTP_201_CREATED)
def register(body:UserSchema, db= Depends(get_db)):
    return userController.register(body,db)