from fastapi import  Depends , HTTPException, status , Path , APIRouter
from models import Todos
from database import engine, session_local
from typing import Annotated
from sqlalchemy.orm import Session 
from pydantic import BaseModel, Field
from .auth import get_current_user
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
    
    
    