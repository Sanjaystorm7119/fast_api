from .utils import *

from ..routers.auth import get_current_user,get_db, authenticate_user

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

