class Enemy :
    def __init__(self, enemy_type: str = "base", health_point: int = 100, attack_damage: int=10):
        """
        constructors are used to create and initialise an object of a class with or without starting values


        types : default/empty -> created automatically if no __init__ , pass in body ,
        no args -> same as default but has a body ir not pass, 
        args -> params are passed (overrides the one in default)

        self : current class
        """
        self.__enemy_type = enemy_type
        self.__health_point = health_point
        self.attack_damage = attack_damage

    def talk(self):
        print(f"the {self.__enemy_type} is screaming")

    def movement(self):
        print(f"the {self.__enemy_type} is moving forward")
    
    def attack(self):
        print(f"the {self.__enemy_type} attacks with {self.attack_damage} damage")

    def health_points(self):
        print(f"the {self.__enemy_type} has {self.__health_point} health points")

    def special_attack(self):
        print(f"the enemy {self.__enemy_type} has no special attack")
# """
# encapsulation => bundling of data  ie enemy_type = "base", health_point = 100, attack_damage=10: 
# to avoid confusion , to prevent object from getting changed, use (__) => private 
# issue ? we cant change data ? so ?
# use getter / setter  
# use @property , highly recommended


# """

#Getter
    @property
    def get_type(self):
        return self.__enemy_type
    
    @property
    def health_points(self):
        return self.__health_point

    @health_points.setter
    def health_points(self, value):
        self.__health_point = value
"""
inheritance : the process of acquiring properties from one class to another

"""