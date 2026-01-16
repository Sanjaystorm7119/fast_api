from .database import Base
from sqlalchemy import Column,Integer , String, Boolean ,ForeignKey


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True , index= True)
    user_name = Column(String, unique=True)
    email = Column(String , unique= True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_pass = Column(String)
    is_active = Column(Boolean)
    role = Column(String, default="user")
    phone_number = Column(Integer)




class Todos(Base):
    __tablename__ = 'todos'  #name of table
    id = Column(Integer , primary_key= True , index = True)
    
    # title = Column(String) #postgre len req for mysql string
    title = Column(String(500)) 
    
    # description = Column(String)#len req for mysql string
    description = Column(String(500))

    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    
