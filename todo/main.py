from fastapi import FastAPI 
# from models import Todos
from .models import Base
from .database import engine 
from .routers import auth , todos , admin , users
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
# models.Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)



@app.get('/health')
async def health_check():
    return {"message":"healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


