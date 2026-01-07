# SQLAlchemy SQLite Todo App (Basic Setup)

This project demonstrates a **basic SQLAlchemy setup using SQLite**.  
It covers how to:

- Create a database engine
- Configure a session
- Define ORM models
- Create tables
- Perform basic database operations

This setup is commonly used with **FastAPI**, but it also works as a standalone Python script.

---

## 📦 Requirements

Make sure you have Python 3.8+ installed.

Install dependencies:

```bash
pip install sqlalchemy
🗂 Project Structure

.
├── main.py          # Database setup and models
├── todos.db         # SQLite database (auto-created)
└── README.md
⚙️ Database Configuration
1. Create Database Engine
python

from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
Explanation:

Uses SQLite as the database

check_same_thread=False is required for multi-threaded apps (e.g. FastAPI)

2. Create Session Factory
python

from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Explanation:

Sessions manage database transactions

autocommit=False → manual commits

autoflush=False → manual flushing

3. Create Base Class
python

from sqlalchemy.orm import declarative_base

Base = declarative_base()
Explanation:

All ORM models inherit from Base

SQLAlchemy uses this to create tables

🧱 Defining a Model (Table)
python

from sqlalchemy import Column, Integer, String, Boolean

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)
Explanation:

Each class represents a database table

Each Column represents a table column

🏗 Create Database Tables
python

Base.metadata.create_all(bind=engine)
Explanation:

Creates tables in todos.db if they do not exist

Safe to run multiple times

🔄 Using the Database Session
Create a Session
python

db = SessionLocal()
Always close the session:

python

db.close()
✍️ Insert Data Example
python

new_todo = Todo(title="Learn SQLAlchemy", completed=False)

db.add(new_todo)
db.commit()
db.refresh(new_todo)
🔍 Query Data Example
python

todos = db.query(Todo).all()

for todo in todos:
    print(todo.id, todo.title, todo.completed)
✅ Key Concepts Summary
Concept	Description
Engine	Database connection
Session	Handles DB operations
Base	Parent for ORM models
Model	Represents DB tables
commit()	Saves changes
query()	Reads data


-------------------------

.mode column / table / box
can be of : 
ascii box column csv html insert json line list markdown qbox quote table tabs tcl