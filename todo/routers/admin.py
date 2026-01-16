from fastapi import  Depends , HTTPException, status , Path , APIRouter 
from ..models import Todos, Users
from ..database import engine, session_local
from typing import Annotated , Optional
from sqlalchemy.orm import Session 
from pydantic import BaseModel, Field , EmailStr
from .auth import get_current_user, bcrypt_context
# from routers import auth

router = APIRouter(
    prefix='/admin',
    tags=['admin']

)
def get_db():
    db = session_local()
    try :
        yield db 
    finally :
        db.close()

        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class ResetPasswordRequest(BaseModel):
    new_password: str = Field(min_length=4)

@router.get('/todo' , status_code=status.HTTP_200_OK)
async def read_all(user : user_dependency , db : db_dependency):
    if user is None or user.get('user_role') != "admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication failed")
    return db.query(Todos).all()

@router.delete('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(user : user_dependency , db: db_dependency , todo_id : int = Path(gt=0)):
    if user is None or user.get('user_role') != "admin" :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication failed")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

@router.put('/reset-password/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(user: user_dependency, db: db_dependency, reset_request: ResetPasswordRequest, user_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication failed")
    user_model = db.query(Users).filter(Users.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    user_model.hashed_pass = bcrypt_context.hash(reset_request.new_password)
    db.commit()
    
