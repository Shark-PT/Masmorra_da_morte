class Enemy:
    def __init__(self):
        raise NotImplementedError("Do not create raw Enemy Objects.")
    
    def __str__(self):
        return self.name
    
    def is_alive(self):
        return self.hp > 0
    
class GiantSpider(Enemy):
    def __init__(self):
        self.name = "Aranha Gigante"
        self.hp = 10
        self.damage = 2
        
class Ogre(Enemy):
    def __init__(self):
        self.name = "Ogre"
        self.hp = 30
        self.damage = 10
        
class BatColony(Enemy):
    def __init__(self):
        self.name = "Colonia de Morcegos"
        self.hp = 100
        self.damage = 4
        
class RockMonster(Enemy):
    def __init__(self):
        self.name = "Monstro de Pedra"
        self.hp = 80
        self.damage = 15
        
