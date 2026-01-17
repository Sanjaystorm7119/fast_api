# #create engine 
# from sqlalchemy import create_engine , text
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.pool import StaticPool
# from ..database import Base
# from ..main import app
# from ..routers.todos import get_db , get_current_user
# from fastapi import status
# from fastapi.testclient import TestClient
# from ..models import Todos
# import pytest

# from dotenv import load_dotenv
# load_dotenv()

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos_app_db_test.db'

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False}, poolclass=StaticPool) 

# testing_session_local = sessionmaker(autocommit= False , autoflush=False, bind=engine)

# # Base = declarative_base() #object of db
# Base.metadata.create_all(bind = engine)


# def override_get_db():
#     db = testing_session_local()
#     try :
#         yield db 
#     finally :
#         db.close()

# def override_get_current_user():
#     return {"username":"jay","id":1 , "user_role":"admin"}


# app.dependency_overrides[get_db] = override_get_db
# app.dependency_overrides[get_current_user] = override_get_current_user

# client = TestClient(app)

# @pytest.fixture
# def test_todo():
#     todos = Todos(
#         title = "learn to code",
#         description = "everyday",
#         priority = 5,
#         complete = False,
#         owner_id = 1,
#         # id = 1
#     )

#     db = testing_session_local()
#     db.add(todos)
#     db.commit()
#     # db.rollback()
#     # try:
#     yield todos
#     db.close()
#     # finally:
#     with engine.connect() as connection:
#         connection.execute(text("delete from todos;"))
#         connection.commit()



# def test_read_all_authenticated(test_todo):
#     response = client.get('/')
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()==[{"complete":False ,"title" : "learn to code","description" : "everyday", "id":1 , "owner_id":1, "priority":5}]

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi import status
from fastapi.testclient import TestClient
from ..models import Todos
import pytest

from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos_app_db_test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={'check_same_thread': False}, 
    poolclass=StaticPool
) 

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db 
    finally:
        db.close()


def override_get_current_user():
    return {"username": "jay", "userid": 1, "user_role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
    # Clear the table first
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
    
    # Create test data
    todo = Todos(
        title="learn to code",
        description="everyday",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)  # Get the ID assigned by the database
    db.close()  # Close session immediately after commit
    
    yield todo
    
    # Cleanup after test
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "complete": False,
        "title": "learn to code",
        "description": "everyday", 
        "id": 1,
        "owner_id": 1,
        "priority": 5
    }]