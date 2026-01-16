import pytest

def test_equal_or_not():
    assert 2 == 2
    assert 2 != 1

def test_isinstance():
    assert isinstance("hello", str)
    assert isinstance(10,int)

def test_is_bool():
    assert ("hello" == "world") is False

def test_is_type():
    assert type(10 is int)

def test_greater_than():
    assert 5 > 4

def test_list():
    num_list = [1,2,3,4]
    any_list = [False , False, True]
    #False, 0, None, "", [], {} : falsy
    assert 1 in num_list
    assert all(num_list)
    assert False in any_list
    assert any(any_list)


#object test
class Student:
    def __init__(self, name, age, marks):
        self.name = name
        self.age = age
        self.marks = marks

    def is_passed(self):
        return self.marks >= 40
    
    def is_eligible(self):
        return self.age >= 18


#with fixtures 

@pytest.fixture
def default_student():
    return Student("Sanjay", 18 , 100)


# def test_student_object():
#     student = Student("Sanjay", 20, 80)

#     assert isinstance(student, Student)
#     assert student.name == "Sanjay" , "should be Sanjay"
#     assert student.is_passed(), "should be greater than or equal to 40"
#     assert student.is_eligible() , "should be atleast 18"

#using fixtures
def test_student_object(default_student):
    # student = Student("Sanjay", 20, 80) # not needed 

    assert isinstance(default_student, Student)
    assert default_student.name == "Sanjay" , "should be Sanjay"
    assert default_student.is_passed(), "should be greater than or equal to 40"
    assert default_student.is_eligible() , "should be atleast 18"


class Student_1:
    def __init__(self, first_name : str, last_name:str , major:str ,age : int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.age = age

@pytest.fixture
def default_student_1():
    return Student_1("sanjay","b","cs",25)

def test_student_1(default_student_1):
    assert default_student_1.first_name == "sanjay","should be Sanjay"
    assert default_student_1.last_name == "b" ,"should be b"
    assert default_student_1.major == "cs","should be cs"
    assert default_student_1.age == 25,"should be 25"

        

