import random
from game import location
import game.config as config
import game.display as display
from game.events import *
from game.items import Item
import game.combat as combat

#Map fragment class
class Map_Fragment(Item):
    def __init__(self, id, description):
        super().__init__(f"map_fragment_{id}", 5)  # Fixed string formatting
        self.description = description
        self.found = False  # The fragment is initially hidden

    def find(self):
        if not self.found:
            self.found = True
            display.announce(f"You found a map fragment: {self.description}")
        else:
            display.announce("You already found this map fragment.")

#Full Map Class
class Map(Item):
    def __init__(self):
        super().__init__("Map", 20)
        self.fragments = [
            Map_Fragment(1, "The northern part of the island"), 
            Map_Fragment(2, "The southern part of the island"),
            Map_Fragment(3, "The eastern part of the island"),
            Map_Fragment(4, "The western part of the island")
        ]
    
    def find_fragment(self, fragment_id):
        # Implemented the method to find a specific fragment
        for fragment in self.fragments:
            if fragment.id == fragment_id:
                return fragment
        return None

class Island(location.Location):
    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Lucci's island"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        
        # Note: This will need to be adjusted based on how these classes are instantiated
        island_map = Map()
        player = None  # This should be set to the actual player object
        
        self.locations["beach"] = Beach_with_ship(self)
        self.locations["cave"] = Cave(self, island_map, player)
        self.locations["cliff"] = Cliff(self, island_map, player)
        self.locations["jungle"] = Jungle(self, island_map, player)
        self.locations["lagoon"] = Lagoon(self, island_map, player)
        
        self.starting_location = self.locations["beach"]

    def enter(self, ship):
        display.announce("arrived at an island", pause=False)

class Beach_with_ship(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['south'] = self

    def enter(self):
        display.announce("arrive at the beach. Your ship is at anchor in a small bay to the south.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "south":
            display.announce("You return to your ship.")
            self.main_location.end_visit()

class Cave(location.SubLocation): 
    def __init__(self, main_location, island_map, player):
        super().__init__(main_location)
        self.name = "cave"
        self.island_map = island_map
        self.player = player
        self.enemy = Skeleton("cave monster")
        
    def enter(self):
        display.announce("you enter a dark cave. A terrifying cave monster blocks your path")
        display.announce("Prepare to fight!")
        
        # Simulate combat
        while self.enemy.health > 0 and self.player.health > 0:
            action = input("What will you do? (attack/run): ").strip().lower()
            if action == "attack":
                self.player.attack(self.enemy)
                if self.enemy.health > 0:
                    self.enemy.attack(self.player)
            elif action == "run":
                display.announce("You run back to the beach!", pause=False)
                return

        if self.player.health > 0:
            display.announce("You have defeated the monster!", pause=False)
            display.announce("You find a map fragment on the ground!", pause=False)
            fragment = self.island_map.fragments[0]  # Northern fragment (fragment_id 1)
            fragment.find()
            self.player.add_to_inventory(fragment)
        else:
            display.announce("You are defeated and unable to retrieve the fragment.", pause=False)

class Skeleton(combat.Monster):
    def __init__(self, name):
        attacks = {}
        attacks["Ghostly Blade"] = ["slashes", random.randrange(35,51), (5,15)]
        attacks["Wailing Cut"] = ["slashes", random.randrange(35,51), (1,10)]
        attacks["Anchored Strikes"] = ["strikes", random.randrange(35,51), (1,10)]
       
        super().__init__(name, random.randrange(7,20), attacks, 75 + random.randrange(-10,11)) 
        self.type_name = "Pirate Skeleton"

class Cliff(location.SubLocation):
    def __init__(self, main_location, island_map, player):
        super().__init__(main_location)
        self.name = "cliff"
        self.island_map = island_map
        self.player = player
        self.enemy = Guardian("cliff guardian")

    def enter(self):
        display.announce("You arrive at a steep cliff. A guardian blocks the way to a map fragment!")
        display.announce("Prepare to fight!")
        
        # Simulate combat
        while self.enemy.health > 0 and self.player.health > 0:
            action = input("What will you do? (attack/run): ").strip().lower()
            if action == "attack":
                self.player.attack(self.enemy)
                if self.enemy.health > 0:
                    self.enemy.attack(self.player)
            elif action == "run":
                display.announce("You run back to the beach!", pause=False)
                return

        if self.player.health > 0:
            display.announce("You have defeated the guardian!", pause=False)
            display.announce("You find another map fragment!", pause=False)
            fragment = self.island_map.fragments[1]  # Eastern fragment (fragment_id 2)
            fragment.find()
            self.player.add_to_inventory(fragment)
        else:
            display.announce("You are defeated and unable to retrieve the fragment.", pause=False) 

class Guardian(combat.Monster):
    def __init__(self, name):
        attacks = {}
        attacks["Craggy Crush"] = ["crushes", random.randrange(35,51), (5,15)]
        attacks["Titan's Grasp"] = ["grasped", random.randrange(35,51), (1,10)]
        attacks["Gravelstorm"] = ["stormed", random.randrange(35,51), (1,10)] 

        super().__init__(name, random.randrange(7,20), attacks, 75 + random.randrange(-10,11)) 
        self.type_name = "Cliff Guardian" 

class Jungle(location.SubLocation):
    def __init__(self, main_location, island_map, player):
       super().__init__(main_location)
       self.name = "jungle"
       self.island_map = island_map
       self.player = player
       self.enemy = JungleBeast("jungle beast")

    def enter(self):
        display.announce("You arrive at the jungle. A beast blocks the way to a map fragment!")
        display.announce("Prepare to fight!")
        
        # Simulate combat
        while self.enemy.health > 0 and self.player.health > 0:
            action = input("What will you do? (attack/run): ").strip().lower()
            if action == "attack":
                self.player.attack(self.enemy)
                if self.enemy.health > 0:
                    self.enemy.attack(self.player)
            elif action == "run":
                display.announce("You run back to the beach!", pause=False)
                return

        if self.player.health > 0:
            display.announce("You have defeated the Jungle Beast!", pause=False)
            display.announce("You find the third map fragment hidden under a large rock!", pause=False)
            fragment = self.island_map.fragments[2]  # Southern jungle fragment (fragment_id 3)
            fragment.find()
            self.player.add_to_inventory(fragment)
        else:
            display.announce("You are defeated and unable to retrieve the fragment.", pause=False)

class JungleBeast(combat.Monster):
    def __init__(self, name):
        attacks = {}
        attacks["scratch 1"] = ["scratches", random.randrange(35,51), (5,15)]
        attacks["scratch 2"] = ["scratches", random.randrange(35,51), (1,10)]
        attacks["kick"] = ["kicks", random.randrange(35,51), (1,10)] 

        super().__init__(name, random.randrange(7,20), attacks, 75 + random.randrange(-10,11))
        self.type_name = "Jungle Beast"

class Lagoon(location.SubLocation):
    def __init__(self, main_location, island_map, player):
        super().__init__(main_location)
        self.name = "lagoon"
        self.island_map = island_map
        self.player = player
        self.enemy = LagoonBeast("Lagoon Serpent")

    def enter(self):
        display.announce("You arrive at a tranquil lagoon, but suddenly the waters stir!")
        display.announce("A massive Lagoon Serpent emerges, blocking your way to the final map fragment!")
        display.announce("Prepare for an intense battle!")
        
        # Simulate combat
        while self.enemy.health > 0 and self.player.health > 0:
            action = input("What will you do? (attack/run): ").strip().lower()
            if action == "attack":
                self.player.attack(self.enemy)
                if self.enemy.health > 0:
                    self.enemy.attack(self.player)
            elif action == "run":
                display.announce("You run back to the beach!", pause=False)
                return

        if self.player.health > 0:
            display.announce("You have defeated the Lagoon Serpent!", pause=False)
            display.announce("You find the final map fragment!", pause=False)
            fragment = self.island_map.fragments[3]  # Western fragment (fragment_id 4)
            fragment.find()
            self.player.add_to_inventory(fragment)
        else:
            display.announce("You are defeated and unable to retrieve the fragment.", pause=False)

class LagoonBeast(combat.Monster):
    def __init__(self, name):
        attacks = {}
        attacks["Boggy Grasp"] = ["Grasps", random.randrange(35,51), (5,15)]
        attacks["Snapping Maw"] = ["Snapping", random.randrange(38,64), (8,18)]
        attacks["Fang-Soaked Bite"] = ["Bites", random.randrange(36,55), (6,16)]
        attacks["Silt Storm"] = ["Stormed", random.randrange(30,45), (4, 14)]

        super().__init__(name, random.randrange(7,20), attacks, 75 + random.randrange(-10,11))
        self.type_name = "Lagoon Serpent"