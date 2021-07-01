from player import Player
import world
from collections import OrderedDict
from colorama import init, Fore, Back, Style
from termcolor import colored
        

def play():
    print("Bem vindo a Masmorra da Morte!!")
    print("\033[31m" + " Bem Vindo á MASMORRA DA MORTE")
    #print('\033[39m')
    print("")
    print(colored("Como the chamas?", "red", "on_blue"))
    nome = input(">")
    
    print("Bem vindo, ", nome)
    world.parse_world_dsl()
    player = Player()
    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        print(room.intro_text())
        room.modify_player(player)
        if player.is_alive() and not player.victory:
            choose_action(room, player) 
        elif not player.is_alive():
            print("A tua jornada chegou ao fim prematuramente")   
    
def get_available_action(room, player):
    actions = OrderedDict()
    print("\nO que queres fazer: ")
    if player.inventory:
        action_adder(actions, 'i', player.print_inventory, "Ver inventario")
        if isinstance(room, world.TraderTile):
            action_adder(actions, "t", player.trade, "Trocar")
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack, "Atacar")
    else:
        if world.tile_at(room.x, room.y -1):
            action_adder(actions, "n", player.move_north, "ir para norte")
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, "s", player.move_south, "ir para sul")
        if world.tile_at(room.x +1, room.y):
            action_adder(actions, "e", player.move_east, "ir para este")
        if world.tile_at(room.x -1, room.y):
            action_adder(actions, "w", player.move_west, "ir para oeste")
    if player.hp <100:
        action_adder(actions, "h", player.heal, "curar")
        
    return actions

def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    print("{}: {}".format(hotkey, name))
    
def choose_action(room, player):
    action = None
    while not action:
        available_actions = get_available_action(room, player)
        action_input = input("Que vais fazer: ")
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print("Ação Invalida!!")
            
    
    
    
play()