from enemy import *
from zombie import Zombie
from ogre import Ogre
from hero import *
# zombie = Enemy("zombie",100,5)

# zombie.talk()
# ogre.talk()

def battle(e1: Enemy , e2: Enemy):
    e1.talk()
    e2.talk()

    while e1.health_points > 0 and e2.health_points > 0 :
        e1.special_attack()
        e2.special_attack()
        print(f"{e1.get_type} : {e1.health_points} HP left")
        print(f"{e2.get_type} : {e2.health_points} HP left")
        e2.attack()
        e1.health_points-=e2.attack_damage
        e1.attack()
        e2.health_points-=e1.attack_damage

    if e1.health_points > 0 :
        print(f"{e1.get_type} wins")
    else :
        print(f"{e2.get_type} wins")

zombie = Zombie(100,5)
ogre = Ogre(150,20)


def hero_battle(hero: Hero , enemy: Enemy):

    while hero.health_points > 0 and enemy.health_points > 0 :
        # hero.special_attack()
        # e2.special_attack()
        print(f"{hero.health_points} HP left")
        print(f"{enemy.get_type} : {enemy.health_points} HP left")
        enemy.attack()
        hero.health_points-=enemy.attack_damage
        hero.attack()
    
        enemy.health_points-=hero.attack_damage

    if hero.health_points > 0 :
        print(f"hero wins")
    else :
        print(f"{enemy.get_type} wins")

zombie = Zombie(100,5)
ogre = Ogre(150,20)
hero = Hero(100,5)
weapon = Weapon('sword',5)
hero.weapon = weapon
hero.equip_weapon()

hero_battle(hero,zombie)

# battle(zombie , ogre)
# battle(ogre)
# 