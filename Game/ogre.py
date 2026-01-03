from enemy import *
import random

class Ogre(Enemy) :
    def __init__(self , health_point , attack_damage ):
        super().__init__(enemy_type='Ogre', 
                         health_point=health_point, 
                         attack_damage=attack_damage)
        
    def talk(self):
        print("*Slamming Hands.....*")

    
    def special_attack(self):
        did_spl_attack_work = random.random() > 0.50
        if did_spl_attack_work :
            self.attack_damage += 20
            print(f"Damage increased by 20 pts")
