#create engine 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app


from dotenv import load_dotenv
load_dotenv()

SQLALCEMY_DATABASE_URL = 'sqlite:///./todos_app_db_test.db'

engine = create_engine(SQLALCEMY_DATABASE_URL, connect_args={'check_same_thread':False}, poolclass=StaticPool) 

test_session_local = sessionmaker(autocommit= False , autoflush=False, bind=engine)

# Base = declarative_base() #object of db
Base.metadata.create_all(bind = engine)


def override_get_db():
    db = test_session_local()
    try :
        yield db 
    finally :
        db.close()
        
app.dependency_overrides[get_db] = override_get_db
