
import json
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilities')))
from log_system import log

class Weapon:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.price = data.get('price')
        self.required_level = data.get('required_level')
        self.attack = data.get('attack')
        self.critical_chance = data.get('critical_chance')
        self.durability = data.get('durability')
        self.quantity = data.get('quantity')
    def __repr__(self):
        return f"Weapon(id={self.id}, name='{self.name}')"

class Shield:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.price = data.get('price')
        self.required_level = data.get('required_level')
        self.defense = data.get('defense')
        self.hp_max = data.get('hp')
        self.durability = data.get('durability')
        self.quantity = data.get('quantity')
    def __repr__(self):
        return f"Shield(id={self.id}, name='{self.name}')"

class Potion:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.price = data.get('price')
        self.hp = data.get('hp')
        self.durability = data.get('durability')
        self.quantity = data.get('quantity')

    def get_hp(self):
        return self.hp

    def use(self, player):
        player.add_health(self.get_hp())
        log.log(f"{player.get_name()} get healed. +{self.get_hp()}hp",1)
    
    def __repr__(self):
        return f"Potion(id={self.id}, name='{self.name}')"

class Drop:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.price = data.get('price')
        self.required_level = data.get('required_level')
        self.defense = data.get('defense')
        self.hp = data.get('hp')
        self.hp_max = data.get('hp_max')
        self.durability = data.get('durability')
        self.quantity = data.get('quantity')
        self.attack = data.get('attack')
    def __repr__(self):
        return f"Item(id={self.id}, name='{self.name}')"        
        

class Items:
    def __init__(self, weapons_path='resources/weapons.json', shields_path='resources/shields.json', potions_path='resources/potions.json', drop_path='resources/drop.json'):
        self.weapons_path = weapons_path
        self.shields_path = shields_path
        self.potions_path = potions_path
        self.drop_path = drop_path
        self.weapons = self.load_weapons() if weapons_path else []
        self.shields = self.load_shields() if shields_path else []
        self.potions = self.load_potions() if potions_path else []
        self.drop = self.load_drop() if drop_path else []

    def load_weapons(self):
        if not os.path.exists(self.weapons_path):
            return []
        with open(self.weapons_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return [Weapon(w) for w in data]
            except json.JSONDecodeError:
                return []

    def load_shields(self):
        if not os.path.exists(self.shields_path):
            return []
        with open(self.shields_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return [Shield(s) for s in data]
            except json.JSONDecodeError:
                return []
    
    def load_potions(self):
        if not os.path.exists(self.potions_path):
            return []
        with open(self.potions_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return [Potion(w) for w in data]
            except json.JSONDecodeError:
                return []
    def load_drop(self):
        if not os.path.exists(self.drop_path):
            return []
        with open(self.drop_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return [Drop(w) for w in data]
            except json.JSONDecodeError:
                return []
    def get_potion_by_id(self, potion_id):
        for potion in self.potions:
            if potion.id == potion_id:
                return potion
        return None
    def get_drop_by_id(self, drop_id):
        for drop in self.drop:
            if drop.id == drop_id:
                return drop
        return None
    

    def get_all_weapons(self):
        return self.weapons

    def get_weapon_by_id(self, weapon_id):
        for weapon in self.weapons:
            if weapon.id == weapon_id:
                return weapon
        return None

    def get_all_shields(self):
        return self.shields

    def get_shield_by_id(self, shield_id):
        for shield in self.shields:
            if shield.id == shield_id:
                return shield
        return None

# Example usage:
# items_list = Items()
# shield = items_list.get_shield_by_id(1)
# if shield:
#     print(shield.name)
#     print(shield.defense)
#     print(shield.price)
#     print(shield.description)
# else:
#     print("No shield with the given id.")