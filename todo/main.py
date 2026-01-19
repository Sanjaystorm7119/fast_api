from fastapi import FastAPI , Request
# from models import Todos
from .models import Base
from .database import engine 
from .routers import auth , todos , admin , users
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
# models.Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="todo/templates")


@app.get('/')
def test(request : Request):
    return templates.TemplateResponse("home.html",{"request" : request}) 

@app.get('/health')
async def health_check():
    return {"message":"healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


