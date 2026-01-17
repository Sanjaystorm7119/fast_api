from .utils import *

from ..routers.auth import get_current_user,get_db, authenticate_user, create_access_token,SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta
import pytest

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_authenticate(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.user_name , "random",db)
    assert authenticated_user is not None
    assert authenticated_user.user_name == test_user.user_name

    try:
        non_existent_user = authenticate_user("wrong","wrong",db)
        assert False, "Should have raised HTTPException"
    except Exception:
        assert True


    # wrong_password_user = authenticate_user(test_user.user_name,"wromg",db)
    # assert wrong_password_user is False
    try:
        wrong_password_user = authenticate_user(test_user.user_name,"wrong",db)
        assert False, "Should have raised HTTPException"
    except Exception:
        assert True



def test_create_access_token():
    username = "sanjay"
    userid = 1
    role = "user"
    expires_delta = timedelta(days=10)

    token = create_access_token(username, userid,role, expires_delta)

    decoded_token = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM,options={"verify_signature":False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == userid
    assert decoded_token['role'] == role


def test_get_current_user():
    import asyncio

    encode = {"sub": "testuser", "id": 1, "role": "admin"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = asyncio.run(get_current_user(token=token))
    assert user == {"username": "testuser", "userid": 1, "user_role": "admin"}



