#create engine 
from sqlalchemy import create_engine


SQLALCEMY_DATABASE_URL = 'sqlite.///./todos.py'


engine = create_engine(SQLALCEMY_DATABASE_URL, connect_args={'check_same_thread':False})