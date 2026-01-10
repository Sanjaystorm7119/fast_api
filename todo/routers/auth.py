from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from models import Users


# app = FastAPI()  # use router for routing
router = APIRouter()

class Create_user_request(BaseModel):
    user_name : str
    email : str
    first_name : str
    last_name : str
    password : str
    role : str

@router.get('/auth')
async def get_user():
    return {"user" : "authenticated"}


@router.post('/auth')
def create_user(create_user_request : Create_user_request):
    # create_user_model = Users(**create_user_request.model_dump()) => since password and hashed+password are differenct

    create_user_model = Users(
        user_name = create_user_request.user_name,
        email = create_user_request.email,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_pass = create_user_request.password,
        is_active = True
        )
    
    return create_user_model

   
"""
create_user_request starts as a Pydantic model (Create_user_request)
.model_dump() converts it to a dict
Users(**...) creates a new Users object (likely a SQLAlchemy model)
"""