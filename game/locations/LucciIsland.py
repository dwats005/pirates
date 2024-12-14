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
        super().__init__(f"map_fragment_{id}", 5)  
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
        self.is_complete = False

    def assemble(self):
        if all(fragment.found for fragment in self.fragments):
            self.is_complete = True
            display.announce("You have assembled all the map fragments into a full map!", pause=False)
        else:
            display.announce("You don't have all the map fragments yet.", pause=False)

    def add_fragment(self, id, description):
        self.fragments.append(Map_Fragment(id, description))
        display.announce(f"A new map fragment was added: {description}")

    def remove_fragment(self, id):
        self.fragments = [f for f in self.fragments if f.id != id]
        display.announce(f"Map fragment with ID {id} was removed.")

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

        self.island_map = Map()
        self.player = None  # This should be set to the actual player object

        self.initialize_locations()

    def initialize_locations(self):
        self.locations = {
            "beach": Beach_with_ship(self),
            "cave": Cave(self, self.island_map, self.player),
            "cliff": Cliff(self, self.island_map, self.player),
            "jungle": Jungle(self, self.island_map, self.player),
            "lagoon": Lagoon(self, self.island_map, self.player),
            "treasure_site": TreasureSite(self, self.player),
        }
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

class Weapon(Item):
    def __init__(self, name, damage):
        super().__init__(name, value=damage * 10)
        self.damage = damage

    def use(self):
        display.announce(f"You wield the {self.name}, increasing your attack power by {self.damage}.")

class Armor(Item):
    def __init__(self, name, defense):
        super().__init__(name, value=defense * 15)
        self.defense = defense

    def use(self):
        display.announce(f"You equip the {self.name}, reducing incoming damage by {self.defense}.")

class Cave(location.SubLocation): 
    def __init__(self, main_location, island_map, player):
        super().__init__(main_location)
        self.name = "cave"
        self.island_map = island_map
        self.player = player
        self.enemy = Skeleton("Cave Monster")
        self.reward_weapon = Weapon("Bone Club", damage=15)  # New weapon
        self.reward_armor = Armor("Ragged Cloak", defense=5)  # New armor

        
    def enter(self):
        display.announce("You enter a dark cave. A terrifying cave monster blocks your path!")
        display.announce("Prepare to fight!")

        # Combat Simulation
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
            display.announce("You have defeated the Cave Monster!", pause=False)
            display.announce("You find a map fragment and powerful items on the ground!", pause=False)
            fragment = self.island_map.fragments[0]  # Northern fragment
            fragment.find()
            self.player.add_to_inventory(fragment)
            self.player.add_to_inventory(self.reward_weapon)
            self.player.add_to_inventory(self.reward_armor)
            display.announce(f"You gained {self.reward_weapon.name} and {self.reward_armor.name}!")
        else:
            display.announce("You are defeated and unable to retrieve the items.", pause=False)


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
        self.enemy = Guardian("Cliff Guardian")
        self.reward_weapon = Weapon("Stone Hammer", damage=20)
        self.reward_armor = Armor("Rockplate Shield", defense=10)


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
            display.announce("You have defeated the Cliff Guardian!", pause=False)
            display.announce("You find a map fragment and rare items!", pause=False)
            fragment = self.island_map.fragments[1]  # Eastern fragment
            fragment.find()
            self.player.add_to_inventory(fragment)
            self.player.add_to_inventory(self.reward_weapon)
            self.player.add_to_inventory(self.reward_armor)
            display.announce(f"You gained {self.reward_weapon.name} and {self.reward_armor.name}!")
        else:
            display.announce("You are defeated and unable to retrieve the items.", pause=False)

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
        self.enemy = JungleBeast("Jungle Beast")
        self.reward_weapon = Weapon("Vine Whip", damage=18)
        self.reward_armor = Armor("Leafmail Armor", defense=7)
        
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
            display.announce("You find the third map fragment and powerful items hidden under a rock!", pause=False)
            fragment = self.island_map.fragments[2]  # Southern fragment
            fragment.find()
            self.player.add_to_inventory(fragment)
            self.player.add_to_inventory(self.reward_weapon)
            self.player.add_to_inventory(self.reward_armor)
            display.announce(f"You gained {self.reward_weapon.name} and {self.reward_armor.name}!")
        else:
            display.announce("You are defeated and unable to retrieve the items.", pause=False)


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
        self.reward_weapon = Weapon("Water Blade", damage=22)
        self.reward_armor = Armor("Aquatic Shell", defense=8)

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
            display.announce("You find the final map fragment and rare treasures!", pause=False)
            fragment = self.island_map.fragments[3]  # Western fragment
            fragment.find()
            self.player.add_to_inventory(fragment)
            self.player.add_to_inventory(self.reward_weapon)
            self.player.add_to_inventory(self.reward_armor)
            display.announce(f"You gained {self.reward_weapon.name} and {self.reward_armor.name}!")
        else:
            display.announce("You are defeated and unable to retrieve the items.", pause=False)

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

class TreasureSite(location.SubLocation):
    def __init__(self, main_location, player):
        super().__init__(main_location)
        self.name = "treasure site"
        self.player = player
        self.final_boss = FinalBoss("Captain Dreadbeard")

    def enter(self):
        display.announce("You arrive at the treasure site, guided by the completed map!")
        display.announce("A puzzle awaits to unlock the exact treasure location.")
        if self.solve_puzzle():
            display.announce("The ground trembles and reveals a hidden cavern where the treasure lies!")
            display.announce("Suddenly, the infamous Captain Dreadbeard appears, guarding the treasure!")
            self.fight_final_boss()
        else:
            display.announce("You failed to solve the puzzle. The treasure remains hidden.", pause=False)

    def solve_puzzle(self):
        puzzle_question = "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?"
        display.announce("Solve the riddle to find the treasure:\n" + puzzle_question)
        attempts = 3
        while attempts > 0:
            answer = input("Your answer: ").strip().lower()
            if answer == "echo":
                display.announce("Correct! You have solved the puzzle.", pause=False)
                return True
            else:
                attempts -= 1
                display.announce(f"Incorrect! {attempts} attempts remaining.")
        return False

    def fight_final_boss(self):
        display.announce("Prepare for the ultimate battle!")
        while self.final_boss.health > 0 and self.player.health > 0:
            action = input("What will you do? (attack/run): ").strip().lower()
            if action == "attack":
                self.player.attack(self.final_boss)
                if self.final_boss.health > 0:
                    self.final_boss.attack(self.player)
            elif action == "run":
                display.announce("You retreat, leaving the treasure behind!", pause=False)
                return
        if self.player.health > 0:
            display.announce("You have defeated Captain Dreadbeard!", pause=False)
            self.claim_treasure()
        else:
            display.announce("You are defeated. The treasure remains out of reach.", pause=False)

    def claim_treasure(self):
        display.announce("You open the treasure chest and find riches beyond your imagination!", pause=False)
        display.announce("You also find new weapons and armor to aid in your future adventures!", pause=False)
        # Example of treasure loot
        self.player.add_to_inventory(Item("Golden Cutlass", 100))
        self.player.add_to_inventory(Item("Enchanted Armor", 150))

class FinalBoss(combat.Monster):
    def __init__(self, name):
        attacks = {
            "Shadow Strike": ["slashes", random.randrange(40, 60), (8, 15)],
            "Cursed Cannonball": ["launches", random.randrange(50, 70), (10, 20)],
            "Ghostly Roar": ["terrifies", random.randrange(30, 50), (5, 10)],
        }
        super().__init__(name, random.randrange(20, 30), attacks, 150 + random.randrange(-20, 20))
        self.type_name = "Ghostly Pirate Captain"

