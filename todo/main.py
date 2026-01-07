from fastapi import FastAPI , Depends
from models import Todos
import models
from database import engine, session_local
from typing import Annotated
from sqlalchemy.orm import Session 
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try :
        yield db 
    finally :
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
@app.get("/")
async def read_all(db : db_dependency):   
    return db.query(Todos).all()
