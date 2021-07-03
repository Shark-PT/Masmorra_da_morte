import items


class NonPlayableCharacter():
    def __init__(self):
        raise NotImplementedError("Não cries objectos de NPC sem ser numa subclasse")
    
    def __str__(self):
        return self.name
    

class Trader(NonPlayableCharacter):
    def __init__(self):
        self.name = "Trader"
        self.gold = 100
        self.inventory = [items.CrustyBread(),
                          items.CrustyBread(),
                          items.Apple(),
                          items.Apple(),
                          items.Apple(),
                          items.HealingPotion(),
                          items.HealingPotion(),
                          items.RustySword()]
        
