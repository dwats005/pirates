from game import location
import game.config as config
import game.display as display
from game.events import *
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu

#Map fragment class
class Map_Fragment(Item):
    def __init__(self, id, description):
        super().__init__("map_fragment_{id}", 5) #Note:each fragment has a unique name and different values
        self.description = description
        self.found = False #The fragment is initially hidden

    def find(self):
        if not self.found:
            self.found = True
            display.announce (f"You found a map fragment: {self.found}")
        else:
            display.announce (f"You already found this map fragment.")

#Full Map Class
class Map(Item):
    def __init__ (self):
        super(). __init__("Map", 20)
        self.fragments = [
            Map_Fragment(1, "The norhern part of the island"), 
            Map_Fragment(2, "The southern part of the island"),
            Map_Fragment(3, "The eastern part of the island"),
            Map_Fragment(4, "The western part of the island")
        ]
    def find_fragment(self, fragment_id):
        fragment = ()
        pass



class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Lucci's island"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach_with_ship(self)
        self.starting_location = self.locations["beach"]
        #self.

    def enter (self, ship):
        display.announce ("arrived at an island", pause=False)

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['south'] = self

    def enter (self):
        display.announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()

class Cave(location.SubLocation): 
    def __init__(self, main_location, island_map, player):
        super().__init__(main_location)
        self.name = "cave"
        self.island_map = island_map
        self.player = player
        self.enemy = Enemy("cave monster", 50) #adding the cave monster
        
    def enter(self):
        display.announce("you enter a dark cave. A terrifying cave monster blocks your path")
        display.announce("Prepare to fight!")
        
      

class Skeleton(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["slash 1"] = ["slashes", random.randrange(35,51), (5,15)]
        attacks["slash 2"] = ["slashes", random.randrange(35,51), (1,10)]
        attacks["shank"] = ["shanks", random.randrange(35,51), (1,10)]
       
        super().__init__(name, random.randrange(7,20), attacks, 75 + random.randrange(-10,11)) 
        self.type_name = "Black Bear"
        