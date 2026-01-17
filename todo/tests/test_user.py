from .utils import *
from ..routers.users import get_current_user,get_db
from fastapi import status


app.dependency_overrides[get_db]= override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user

def test_user(test_user):
    response = client.get('/user/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['user_name']=='sanjay'
    assert response.json()['email']=='leaabcd@gmail.com'
    assert response.json()['first_name']=='sanjay'
    assert response.json()['last_name']=='jaysan'
    assert response.json()['role']=='admin'
    assert response.json()['phone_number']=='111-111-1111'

    """
    never expose password : below is just to verify
    """
    
    assert bcrypt_context.verify("random",response.json()['hashed_pass'])

    

def test_update_password_success(test_user):
    response = client.put('/user/password',json={"password":"random", "new_password":"new_test"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_password_invalid(test_user):
    response = client.put('/user/password',json={"password":"new", "new_password":"new_test"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail":"unauthorised"}


def test_update_phone_number_invalid(test_user):
    response = client.put('/user/phone_number/1111111111')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # assert response.json() == {"detail":"unauthorised"}
