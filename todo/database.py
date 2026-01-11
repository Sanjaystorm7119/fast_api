#create engine 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


SQLALCEMY_DATABASE_URL = 'sqlite:///./todos_app_db.db'


engine = create_engine(SQLALCEMY_DATABASE_URL, connect_args={'check_same_thread':False})

"""
engine = create_engine(SQLALCEMY_DATABASE_URL, connect_args={'check_same_thread': False})
create_engine() creates a connection engine to the database.
SQLALCEMY_DATABASE_URL is a string containing the database URL
(example: "sqlite:///./test.db").
connect_args={'check_same_thread': False}:
This is specific to SQLite.
SQLite normally allows database access only from the same thread.
Setting this to False allows the database to be accessed from multiple threads (needed for FastAPI).
The engine is responsible for:
Managing database connections
Sending SQL queries to the database

"""

session_local = sessionmaker(autocommit= False , autoflush=False, bind=engine)

"""
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
sessionmaker() creates a factory for database sessions.
session_local is not a session yet, but a session creator.
Arguments explained:
autocommit=False
You must explicitly call commit() to save changes.
autoflush=False
Changes are not automatically sent to the database until you call flush() or commit().
bind=engine
Tells SQLAlchemy which database engine to use.
Each request will usually create its own session using:
db = session_local()
"""

Base = declarative_base() #object of db

"""
declarative_base() creates a base class for ORM models.
Base is used to:
Define database tables as Python classes.
Store metadata about all tables.
"""


"""
url->engine->session->base class->model table->create db
"""