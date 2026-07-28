from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.utils.settings import settings
from datetime import datetime
from src.user.userModels import UserModel
from jwt import InvalidTokenError
from src.utils.db import get_db
import jwt



def is_authenticated(request:Request,db:Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")
        token = token.split(" ")[-1]

        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        #print(data)
        user_id = data.get("_id")
        exp_time = data.get("exp_time")

        current_time = datetime.now().timestamp()
        if current_time  > exp_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized") 
        
        return user
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized")