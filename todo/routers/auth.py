from fastapi import FastAPI, APIRouter , Depends , status , HTTPException
from typing import Annotated
from database import session_local
from pydantic import BaseModel , Field , EmailStr
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer 
from jose import jwt , JWTError
from datetime import timedelta , datetime , timezone
from dotenv import load_dotenv
load_dotenv()
import os



bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2password_bearer = OAuth2PasswordBearer(tokenUrl = 'auth/token')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')




# app = FastAPI()  # use router for routing
router = APIRouter(
    prefix='/auth',
    tags=['auth']

)
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

class Token(BaseModel):
    access_token : str
    token_type : str


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



def authenticate_user(user_name : str , password : str , db : Session):
    user = db.query(Users).filter(Users.user_name == user_name).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    if not bcrypt_context.verify(password , user.hashed_pass):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid password")
    return user

def create_access_token(username: str , userid : int , expires_delta : timedelta):
    encode = {
        "sub": username , "id" :userid
    }
    expires =  datetime.now(timezone.utc)+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token : Annotated[str, Depends(oauth2password_bearer)]):
    try :
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        userid : int = payload.get('id')
        if username is None or userid is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized")
        return {"username" : username , "userid" : userid}
    except :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="unauthorized")




@router.get('/')
async def get_user():
    return {"user" : "authenticated"}


@router.post('/',status_code=status.HTTP_201_CREATED)
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

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()],db: db_dependency):
    user =  authenticate_user(form_data.username, form_data.password , db)
    if not user :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authorised")
    token = create_access_token(user.user_name , user.id, timedelta(minutes=20))
    
    # return {f"user_name : {form_data.username} , authentication successful , token :{token}"}
    return {"access_token" : token , "token_type":'bearer'}