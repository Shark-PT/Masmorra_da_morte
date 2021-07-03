import items
import world



class Player:
    def __init__(self):
        self.inventory = [items.Rock(),
                          items.Dagger(),
                          items.CrustyBread(),
                          items.Apple()]
        
        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.hp = 100
        self.gold = 5
        self.victory = False
        
    def is_alive(self):
        return self.hp > 0
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def move_north(self):
        self.move(dx = 0, dy = -1)
        
    def move_south(self):
        self.move(dx = 0, dy = 1)
        
    def move_east(self):
        self.move(dx = 1, dy = 0)
        
    def move_west(self):
        self.move(dx = -1, dy = 0)

    #def pick_item(self):
    #    room = world.tile_at(self.x, self.y)
    #    self.room.modify_player
    
    def print_inventory(self):
        print("\nInventario:")
        for item in self.inventory:
            print('* ' + str(item))
        print("Ouro: {}". format(self.gold))
            
    def heal(self):
        consumables = [item for item in self.inventory if isinstance(item, items.Consumable)]
        if not consumables:
            print("Tu não tens nenhum item de cura!")
            return
        
        for i, item in enumerate(consumables, 1):
            print("Escolhe um item para te curar: ")
            print("{}. {}".format(i, item))
            
        valid = False
        while not valid:
            choice = input (" ")
            try:
                to_eat = consumables[int(choice) - 1]
                self.hp = min(100, self.hp + to_eat.healing_value)
                self.inventory.remove(to_eat)
                print("Pontos de vida que tens: {}". format(self.hp))
                valid = True
            except (ValueError, IndexError):
                print("Escolha invalida. Tenta outra vez.")

    
    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
            try:
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
            except AttributeError:
                pass

        return best_weapon
    
    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        print("\nTu usas {} contra {}!".format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("\nMataste {}!".format(enemy.name))
        else:
            print("{} HP é {}.".format(enemy.name, enemy.hp))
            
    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self)