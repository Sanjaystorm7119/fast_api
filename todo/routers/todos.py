from fastapi import  Depends , HTTPException, status , Path , APIRouter
from models import Todos
from database import engine, session_local
from typing import Annotated
from sqlalchemy.orm import Session 
from pydantic import BaseModel, Field
from .auth import get_current_user
# from routers import auth

router = APIRouter()
# router.include_router(auth.router)
# models.Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try :
        yield db 
    finally :
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class Todo_request(BaseModel):
    title : str = Field(min_length=4)
    description : str = Field(min_length=4)
    priority : int = Field(gt=0, le=5)
    complete : bool 



@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency , db : db_dependency):  
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authorised")
    return db.query(Todos).filter(Todos.owner_id==user.get('userid')).all()

@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def get_todo_by_id(user : user_dependency,db: db_dependency, todo_id : int = Path(gt=0)):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authorised")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('userid')).first()
    if todo_model is not None:
        return todo_model
    else :
        raise HTTPException(status_code=404, detail="not found")


@router.post('/todos', status_code=status.HTTP_201_CREATED)
async def create_new_todo(user : user_dependency,db: db_dependency , todo : Todo_request):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authorised")
    
    todo_model = Todos(**todo.model_dump() , owner_id = user.get('userid'))

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return todo_model


@router.put('/todos/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user : user_dependency,db : db_dependency , todo : Todo_request, todo_id : int = Path(gt=0)):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authorised")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('userid')).first()
    if todo_model is None:
        raise HTTPException(status_code=404 , detail="not found")
    todo_model.title =  todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit() 
    db.refresh(todo_model)



@router.delete("/delete/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user : user_dependency ,db : db_dependency ,todo_id : int = Path(gt=0)):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authorised")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('userid')).first()
    if todo_model is None:
        raise HTTPException(status_code=404 , detail="not found")
    else :
        db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('userid')).delete()

        db.commit()
        


