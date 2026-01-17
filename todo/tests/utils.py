from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
from ..models import Todos
import pytest

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
