from collections import UserString
import enemies
import random
import npc
import items
from colorama import init, Fore, Back, Style
from termcolor import colored

class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def intro_text(self):
        raise NotImplementedError("Cria uma subclass, em vez de outra classe")
    
    def modify_player(self, player):
        pass
    
class CorredorTile(MapTile):
    def intro_text(self):
        return """
        \num corredor escuro encontra-se à tua frente.
        Tens coragem de continuar?"""
        
class HallTile(MapTile):
    def intro_text(self):
        return """
        \num hall enorme está à tua frente com caminhos em frente e para a direita e a esquerda.
        A serio, um cruzamento para confundir ainda mais???
        Só te apetece esganar quem criou esta masmorra"""
        
class CruzamentoDrtFrenteTile(MapTile):
    def intro_text(self):
        return """
        \nOlhas à volta e vês dois caminhos.
        Um para norte e outro para Oeste"""
        
class CruzamentoEsqFrenteTile(MapTile):
    def intro_text(self):
        return """
        \nE para não destoar, mais um cruzamento.
        Agora é para Norte e Este"""
        
    
        
class StartTile(MapTile):
    def intro_text(self):
        return """
        \nNa tua frente tens uns portões ferruguentos que aparentam ter centenas de anos desde que foram abertos
        que misterios, lendas, monstros e tesouros se escondem lá dentro!!!
        Irás descobrir logo que abras os mesmos!!
        """
        
class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.randint(1,10)
        if r < 5:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "\nUma Aranha gigante salta a tua frente " \
                "e lança a teia contra ti"
            self.dead_text = "\n\033[31mO corpo morto da aranha " \
                "apodrece no chão.\033[39m"
        elif r < 8:
            self.enemy = enemies.Ogre()
            self.alive_text = "\nUm Ogre está a bloquear o teu caminho!"
            self.dead_text = "\n\033[31mUm ogre morto no chão relembra-te do teu triunfo\033[39m"
        elif r < 6:
            self.enemy = enemies.BatColony()
            self.alive_text = "\nOuves uns barulhos ao longe" \
                "... até que de repente te vês no meio de um enxame de morcegos!"
            self.dead_text = "\n\033[31mDezenas de morcegos estão espalhados no chão.\033[39m"
        elif r < 3:
            self.enemy = enemies.Bear()
            self.alive_text = "\n Vês um enorme Urso Pardo" \
                "de pé e com cara de quem te quer atacar"
            self.dead_text = "\n\033[31mFicas todo contente ao ver que o urso jaz inaminado no chão"
            
        elif r < 2 :           
            self.enemy = enemies.Goblin()
            self.alive_text = "\nUm Goblin verde e verruguento armado com uma espada"
            self.dead_text = "\n\033[31mmatas o Goblin e vês o sangue verde a escorrer pelo chão\033[39m"
            
        else :
            self.enemy = enemies.RockMonster()
            self.alive_text = "\nTu acordaste um monstro de pedra " \
                "no seu covil!"
            self.dead_text = "\nDerrotado, o monstro reverteu " \
                "para uma rocha normal."
                    
        #else:
        #    self.enemy = enemies.Dragon()
        #    self.alive_text = """\033[31mEncontras-te um dragão gigante. Apesar de todas as tuas tentativas
        #morres queimado pelo mesmo.
        #Foi uma boa viagem, mas acaba aqui.\033[39m""" 
            
        super().__init__(x, y)
        
        
    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text
        
    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage 
            print("\nO inimigo deu-te {} de dano. Tu tens {} HP restantes.".format(self.enemy.damage, player.hp))
        
            
class ItemTile(MapTile):
    def __init__(self, x, y):
        self.item_claimed = False
        self.item = None
        super().__init__(x,y)
        r = random.randint(1,10)
        
        
            
        if r > 8:
            self.item = items.CrustyBread()
            self.description = """  \nEncontras-te um pão duro no chão"""
        elif r > 6:
            self.item = items.Apple()
            self.description = """ \nOlhas para a sala e vês uma maçã"""
        
        elif r > 5:
            self.item = items.HealingPotion()
            self.description = """\nUma poção de vida, que maravilha"""
            
        elif r > 3:
            self.item = items.RustySword()
            self.description = """\nEncontras-te uma espada, vai-te dar bastante jeito"""
        elif r > 2:
            self.item = items.Axe()
            self.description = "\nUm machado perdido, espectaculo!!"
        else:
             self.description = """\nNão encontraste nada!!"""
            
    def intro_text(self,):
        if self.item_claimed:
            return """
                    Já apanhaste o item, não sejas ganante"""
        text = self.description 
        return text
    
    def modify_player(self, player):
        if not self.item_claimed:
            self.item_claimed = True
            if self.item != None:
                player.inventory.append(self.item)
                print("apanhaste {}".format(self.item)) 
            else:
                print("Fica para a proxima")


        
    
class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super().__init__(x,y)
        
    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Ouro".format(i, item.name, item.value))
        while True:
            user_input = input("Escolhe um item ou pressiona Q para sair.")
            if user_input in ["Q", "q"]:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print("Escolha invalida!")
                    
    def swap(self, seller, buyer, item):
        if item.value > buyer.gold:
            print("Isso é muito caro")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold = seller.gold + item.value
        buyer.gold = buyer.gold - item.value
        print("Troca completa!")
        
    def check_if_trade(self, player):
        while True:
            print("Queres Comprar (B), Vender(S) ou Sair(Q)?") 
            user_input = input()
            if user_input in ["Q", "q"]:
                return
            elif user_input in ["B", "b"]:
                print("Isto é o que tenho disponivel: ") 
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ["S", "s"]:
                print("Isto é o que tenho disponivel:")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Escolha invalida!")
    
    def intro_text(self):
        return """
    uma fragil creatura, meio humana, meio bicho está sentada no canto 
    a balançar o seu ouro. Ele parece que está disposto a fazer trocas.
    """
                    
class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__(x,y)
        
    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            print("recebeste mais {} moedas de ouro.".format(self.gold)) 
            
    def intro_text(self):
        if self.gold_claimed:
            return """
        Outra parte normal da masmorra. Tu
        continuas a desbravar caminho
        """
        
        else:
            return"""
        Alguém deixou cair moedas de ouro. Apanhaste-as.
        """
      
class LoseTile(MapTile):
    def modify_player(self,player):
        player.hp = 0
        
    def intro_text(self):
        return """\033[31m
        Caiste num buraco sem fundo.
        ...A serio, um buraco numa masmorra?!?
        rogas pragas a quem contruiu esta masmorra durante a longa queda para um fim inglorio '\033[39m'"""

class DragonTile(MapTile):
    def intro_text(self):
        return """\033[31;43mEncontras-te um dragão gigante. Apesar de todas as tuas tentativas
        morres queimado pelo mesmo.
        Foi uma boa viagem, mas acaba aqui.\033[0;37;40m""" 
    def modify_player(self, player):
        player.hp = 0


    
class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True
        
    def intro_text(self):
        return """
        Tu vês uma luz timida à distancia
        ... Ela aumenta à medida que te aproximas! É a saida
    
    
        Conseguiste sair da masmorra com vida, mais experiente e os bolsos mais cheios!!!
        """

world_dsl = """
|  |  |LT|  |  |  |DG|  |  |  |  |
|  |TT|EF|CT|EN|  |TT|  |  |  |  |
|  |  |  |  |CT|  |CT|  |  |  |FG|
|  |EN|  |CT|FG|EN|HT|CT|EN|HT|EN|
|  |TT|  |FG|  |  |  |CT|  |  |TT|
|  |FG|EN|FG|HT|CT|EN|EF|  |  |EN|
|  |  |FG|  |FG|  |  |FG|  |  |VT|
|DG|  |EN|  |  |  |  |CT|TT|  |  |
|CT|FG|HT|IT|  |  |TT|DF|CT|  |  |
|EN|  |  |CT|EN|CT|HT|  |FG|  |  |
|LT|  |  |  |CT|  |FG|  |  |  |  |
|  |  |  |  |ST|  |  |  |  |  |  |
"""
def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|VT|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False
    return True

#Dicionario que abrevia os nomes das salas para ser mais legivel na grelha
tile_type_dict = {"VT": VictoryTile,
                  "EN": EnemyTile,
                  "ST": StartTile,
                  "FG": FindGoldTile,
                  "TT": TraderTile,
                  "CT": CorredorTile,
                  "DG": DragonTile,
                  "IT": ItemTile,
                  "HT": HallTile,
                  "LT": LoseTile,
                  "DF":CruzamentoDrtFrenteTile,
                  "EF":CruzamentoEsqFrenteTile,
                  "  ": None}
            
world_map = []

start_tile_location = None

def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")
    
    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]
    
    #iterate over each line in the DSL. Instead of i, the variable y is used because we're working with a X-Y grid.
    for y, dsl_row in enumerate(dsl_lines):
        #Create an object to store the tiles
        row = []
        #split the line into abreviations Using the "Split" method
        dsl_cells = dsl_row.split("|")
        #The split method includes the beginning and end of the line so we need to remove Those nonexistent cells
        dsl_cells = [c for c in dsl_cells if c]
        #Iterate over each cell in the DSL line
        #Instead of j, the variable x is used because we're working with an X-Y grid.
        for x, dsl_cell in enumerate(dsl_cells):
            #Look up the abbreviation in the dictionary
            tile_type = tile_type_dict[dsl_cell]
            #Adding the starting points coordinates
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            #If the dictionary returned a valid type, create a new tile object
            #pass it the X-Y coordinates as required by the tile __init__() and add it to the row object.
            #If None was found in the dictionary, we just add None.
            row.append(tile_type(x, y) if tile_type else None)
            
        #Add the whole row to the world_map
        world_map.append(row)

#Função que localiza a sala nas coordenadas
#Sem esta função, o jogo teria que confirmar as coordenadas em cada movimento
def tile_at(x, y):
    if x < 0 or y < 0:         #Se alguma coordenada for negativa, a função não retorna nada. 
        return None            
    try:
        return world_map[y][x] #Se as coordenadas forem validas, retorna a sala que está atribuida à mesma na grelha feita antes
    except IndexError:         #Se as coordenadas forem maiores que os valores do world_dsl, a função não retorna nada
        return None  
    
