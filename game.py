import random
import os
from dataclasses import dataclass
from typing import List, Optional

def process_command(command):
    # Your command handling logic here...
    if command == "start":
        return "Game started! Welcome to the adventure."
    elif command == "look":
        return "You are standing in a dense forest. Paths lead north, south, east, and west."
    # ... add more command handling logic here ...
    else:
        return f"Unknown command: {command}"


@dataclass
class Item:
    name: str
    price: int
    count: int
    description: str

    def use(self, user, enemy):
        pass

    def pack(self, user, backpack):
        backpack.append(self)

    def pic(self):
        pass

@dataclass
class Character:
    name: str
    health: int
    max_health: int
    power: int
    evade: int
    armor: int
    level: int = 1


  

    def print_status(self):
        print(f"The {self.name} has {self.health} health and {self.power} power.")

    def is_alive(self):
        return self.health > 0

    def attack(self, enemy):
        miss = random.randint(1, 100)
        if 1 < miss < (enemy.evade * 5):
            print("The enemy missed!")
        else:
            if enemy.armor > self.power:
                print("The attack doesn't go through your armor!")
            else:
                damage = self.power - enemy.armor
                enemy.health -= damage
                print(f"The {self.name} does {damage} damage to the {enemy.name}. The {enemy.name} has {enemy.health} health left.")

@dataclass
class Hero(Character):
    gold: int = 20

    def attack(self, enemy):
        crit = random.randint(1, 10)
        miss = random.randint(1, 100)
        if 1 < miss < (enemy.evade * 5):
            print("You missed!")
        else:
            if crit < 3:
                if enemy.armor > (self.power * 2):
                    print("It doesn't go through the enemy's armor!")
                else:
                    damage = (self.power * 2) - enemy.armor
                    print("Critical Strike!")
                    enemy.health -= damage
            else:
                super().attack(enemy)

    def __str__(self):
        evade_pct = self.evade * 5
        return f"| Health: {self.health}\n| Max-Health: {self.max_health}\n| Power: {self.power}\n| Evade: {self.evade}({evade_pct}%)\n| Armor: {self.armor}\n| Gold: {self.gold}"

# Add other character classes (Medic, Shadow, Goblin, etc.) here...

def fight_sequence(enemy, hero, backpack):
    while enemy.is_alive() and hero.is_alive():
        print("_" * 83)
        hero.print_status()
        enemy.print_status()
        print("_" * 83)
        print("\nWhat do you want to do?")
        print("1. Fight", enemy.name)
        print("2. Use item")
        print("3. Get status of hero")

        choice = input(" >> ")

        if choice == "1":
            os.system("clear")
            hero.attack(enemy)
            if not enemy.is_alive():
                print("Victory!")
                hero.gold += enemy.gold
                print(f"You found {enemy.gold} gold!")
        elif choice == "2":
            os.system("clear")
            print("Choose an item number to use")
            for i, item in enumerate(backpack):
                print(f"{i}. {item.name}")
            used = int(input(">> "))
            backpack[used].use(hero, enemy)
            del backpack[used]
        elif choice == "3":
            os.system("clear")
            print(hero)
        else:
            print("Invalid input, try again.")

        if enemy.is_alive():
            enemy.attack(hero)
            if not hero.is_alive():
                print("Game Over!")
                exit()

def store(items, hero, backpack):
    while True:
        print("Welcome to the store!")
        print(f"Gold: {hero.gold}")
        for i, item in enumerate(items):
            print(f"{i + 1}. {item}")
        print(f"{len(items) + 1}. Get Hero Status")
        print(f"{len(items) + 2}. Exit")

        choice = input(">> ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(items):
                item = items[choice - 1]
                if item.count > 0 and hero.gold >= item.price:
                    item.pack(hero, backpack)
                    hero.gold -= item.price
                    item.count -= 1
                    print(f"You bought {item.name}")
                elif item.count == 0:
                    print("This item is out of stock.")
                else:
                    print("You don't have enough gold.")
            elif choice == len(items) + 1:
                print(hero)
            elif choice == len(items) + 2:
                break
        else:
            print("Invalid input, please try again.")

def main():
    hero = Hero("Hero", 20, 20, 5, 1, 0)
    backpack = []
    floor_count = 1
    items = [
        Item("Super Tonic", 20, 5, "Brings your character back to max health."),
        Item("Armor Plate", 20, 5, "Adds two armor to your character."),
        # Add other items here...
    ]

    enemies = [
        Character("Goblin", 6, 6, 2, 3, 0),
        Character("Shadow", 1, 1, 1, 18, 0),
        # Add other enemies here...
    ]

    print("Welcome to the Dungeon Crawler!")
    while floor_count < 25:
        print(f"\nFloor #{floor_count}")
        enemy = random.choice(enemies)
        fight_sequence(enemy, hero, backpack)
        store(items, hero, backpack)
        floor_count += 1

    print("Congratulations! You've reached the final boss!")
    # Implement final boss fight here

if __name__ == "__main__":
    main()