manual testing
unit testing
integration testing
system testing

---

##### always begin func name with "test"

assert

Basics :

1. integer
   assert 3==3
2. instance
   assert isInstance("hello",str) true
   assert isInstance("10",str) true
3. bool
   assert ("hello" == "world") is False : true
4. types
   assert type("hello" is str)
5. gt , lt values
   assert 7>8



#pytest objects

class Student:
    def __init__(self, name, age, marks):
        self.name = name
        self.age = age
        self.marks = marks

    def is_passed(self):
        return self.marks >= 40

def test_student_object():
    student = Student("Sanjay", 20, 75)

    assert isinstance(student, Student)


