from enemy import *
import random
class Zombie(Enemy) :
    def __init__(self , health_point , attack_damage ):
        super().__init__(enemy_type='Zombie', 
                         health_point=health_point, 
                         attack_damage=attack_damage)
        
    def talk(self):
        print("*Grumbling.....*")

    def spread_disease(self):
        print("Zombie is tring to spred disease")

    def special_attack(self):
        did_spl_attack_work = random.random() > 0.50
        if did_spl_attack_work :
            self.health_points += 2
            print(f"Zombie regenerated 2 HP")
