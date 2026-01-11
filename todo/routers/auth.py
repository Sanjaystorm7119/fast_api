from fastapi import FastAPI, APIRouter , Depends , status
from typing import Annotated
from database import session_local
from pydantic import BaseModel , Field , EmailStr
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session




bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# app = FastAPI()  # use router for routing
router = APIRouter()
class Create_user_request(BaseModel):
    user_name : str = Field(min_length=2)
    email : EmailStr
    first_name : str = Field(min_length=2 , max_length=20)
    last_name : str = Field(min_length=2 , max_length=20)
    password : str
    role : str = Field(min_length=4)

    model_config = {
        "json_schema_extra" :{
            "example" : {
                "user_name" : "san",
                "email" : "asasa@basas.com",
                "first_name" : "sanj",
                "last_name" : "ayy",
                "password" : "random",
                "role" : "admin"
            }
        }
    }

def get_db():
    db = session_local() #session creator
    try :
        yield db
    # except Exception as e:    # catches errors
    #     db.rollback()         # resets session to clean state
    #     return {"error": f"User creation failed: {str(e)}"}

    finally :
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get('/auth')
async def get_user():
    return {"user" : "authenticated"}


@router.post('/auth',status_code=status.HTTP_201_CREATED)
def create_user(db : db_dependency,create_user_request : Create_user_request):
    # create_user_model = Users(**create_user_request.model_dump()) => since password and hashed+password are differenct
    try :
        create_user_model = Users(
            user_name = create_user_request.user_name,
            email = create_user_request.email,
            first_name = create_user_request.first_name,
            last_name = create_user_request.last_name,
            role = create_user_request.role,
            hashed_pass = bcrypt_context.hash(create_user_request.password),
            is_active = True
            )
        # return create_user_model
        db.add(create_user_model)
        db.commit()
        db.refresh(create_user_model)

        return {
            "id": create_user_model.id,
            "user_name": create_user_model.user_name,
            "email": create_user_model.email,
            "first_name": create_user_model.first_name,
            "last_name": create_user_model.last_name,
            "role": create_user_model.role,
            "is_active": create_user_model.is_active
        }

    except Exception as e:
        db.rollback()
        return {"error": f"User creation failed: {str(e)}"}
    
   
"""
create_user_request starts as a Pydantic model (Create_user_request)
.model_dump() converts it to a dict
Users(**...) creates a new Users object (likely a SQLAlchemy model)
"""

"""
hash -> passlib -> context -> cryptcontext
"""