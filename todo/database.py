#create engine 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


SQLALCEMY_DATABASE_URL = 'sqlite.///./todos.db'


engine = create_engine(SQLALCEMY_DATABASE_URL, connect_args={'check_same_thread':False})

session_local = sessionmaker(autocommit= False , autoflush=False, bind=engine)

Base = declarative_base() #object of db


 



"""
url->engine->session->base class->model table->create db
"""