class Animal :
    def __init__(self):
        pass
    weight : int
    color : str
    animal_type : str

    def eat(self):
        print("Animal eating")

    def sleep(self):
        print("animal sleeping")

    

class Dog(Animal):
    can_shed : bool
    domestic_name : str

    def talk(self):
        print("Dog barking")

    def eat(self):
        print("Dog eating")

dog = Dog()
dog.eat() #present in child (overridden)
dog.sleep() #not in Dog so run Animal (parent)
"""
    method overriding : Animal eat() is generic ? what if Dog has its own eat and own sleep??

    will run parent methods if method is not in child

    will override parent methods if method is present in child

"""

class Bird(Animal):
    bird_type : str

    def talk(self):
        print("chirp")

    def fly(self):
        print("flew")

bird = Bird()
bird.fly()