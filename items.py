class Weapon:
    def ___init__(self):
        raise NotImplementedError("Não cries objectos (armas)")
    
    def __str__(self):
        return self.name
    

class Rock(Weapon):
    def __init__(self):
        self.name = "Pedra"
        self.description = "Uma pedra do tamanho de um punho. Ideal para espancar." 
        self.damage = 5
        self.value = 1
        
class Dagger(Weapon):
    def __init__(self):
        self.name="Adaga"
        self.description = "uma pequena adaga com alguma ferrugem. " \
                           "ligeiramente mais perigosa que uma pedra." 
        self.damage = 10
        self.value = 20

class RustySword(Weapon):
    def __init__(self):
        self.name = "Espada Ferrugenta"
        self.description = "Esta espada já mostra a idade, " \
                           "mas ainda dá luta."
        self.damage = 20
        self.value = 30

class Axe(Weapon):
    def __init__(self):
        self.name = "Machado"
        self.description = "Um machado usado, " \
                           "Quantas arvores já terá cortado e quantos inimigos matado?"
        self.damage = 25
        self.value = 40                   
                           
class Consumable:
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")
    
    def __str__(self):
        return "{} (+{} HP)".format(self.name, self.healing_value)
    
class CrustyBread(Consumable):
    def __init__(self):
        self.name = "Pão Duro"
        self.healing_value = 10
        self.value = 12
        
class Apple(Consumable):
    def __init__(self):
        self.name = "Maça"
        self.healing_value = 5
        self.value = 7
        
class HealingPotion(Consumable):
    def __init__(self):
        self.name = "Poção de vida"
        self.healing_value = 50
        self.value = 35
        
        
            