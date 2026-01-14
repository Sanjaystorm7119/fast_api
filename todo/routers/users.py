from fastapi import  Depends , HTTPException, status , Path , APIRouter 
from models import Todos , Users
from database import engine, session_local
from typing import Annotated , Optional
from sqlalchemy.orm import Session 
from pydantic import BaseModel, Field , EmailStr
from .auth import get_current_user , bcrypt_context
from passlib.context import CryptContext

# from routers import auth

router = APIRouter(
    prefix='/user',
    tags=['user']

)
def get_db():
    db = session_local()
    try :
        yield db 
    finally :
        db.close()

class user_verification(BaseModel):
    password : str 
    new_password : str  = Field(min_length=6)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.get('/',status_code=status.HTTP_200_OK)
async def get_user(user : user_dependency , db : db_dependency ):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication failed")
    return db.query(Users).filter(Users.id == user.get('userid')).first()


@router.put('/password/',status_code=status.HTTP_204_NO_CONTENT)
async def update_user_details(user : user_dependency , db : db_dependency , user_verification : user_verification ):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('userid')).first()
    if not bcrypt_context.verify(user_verification.password , user_model.hashed_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="unauthorised")
    
    user_model.hashed_pass = bcrypt_context.hash(user_verification.new_password)
    db.commit()
    
@router.put("/phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency , db : db_dependency, phone_number : int):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication failed")
    
    user_model = db.query(Users).filter(Users.id == user.get('userid')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()