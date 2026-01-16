test db

create test db
create test dependencies separate from prod dependency
we can do integration testing this way


testing dependencies

1) create new files test_todo.py <-> todo.py
2) create database engine
    from sqlalchemy import create_engine
    sqlalchemy_database_url = "sqlite3///./testdb.db"

3) add new engine
    from sqlalchemy import create_engine
    from sqlalchemy.pool import StaticPool
    sqlalchemy_database_url = "sqlite3///./testdb.db"

    engine = create_engine(sqlalchemy_database_url ,connect_args :{"check_same_thread"=False},
    PoolClass = StaticPool)

4) Add testing session Local
    from sqlalchemy import create_engine
    from sqlalchemy.pool import StaticPool
    from ..database import Base

    sqlalchemy_database_url = "sqlite3///./testdb.db"

    engine = create_engine(sqlalchemy_database_url ,connect_args :{"check_same_thread"=False},
    PoolClass = StaticPool)


    Testing_session_local = sessionmaker(auto_commit=False , auto_flush=False,bind = engine)
    Base.metadata.create_all(bind=engine)

5) set get_testing_db dependency

    def override_get_db():
        db = Testing_session_local
        try :
            yield db

        finally :
            db.close()

    def override_get_current_user():
        return {"user_name":"jay" , "id":1 , "user_role" : "admin"}

    app.dependency_overrides[get_db]= override_get_db
    app.dependency_overrides[get_current_user]= override_get_current_user

6) 
normal
app = FastApi()

test
client = TestClient(app)

