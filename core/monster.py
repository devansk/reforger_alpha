import json
import os
import sys
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilities')))
from log_system import log

class Monsters:
    def __init__(self, monsters_path='resources/monsters.json'):
        self.monsters_path = monsters_path
        self.monsters = self.load_monsters() if monsters_path else []

    def load_monsters(self):
        if not os.path.exists(self.monsters_path):
            return []
        with open(self.monsters_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return [Monster(m) for m in data]
            except json.JSONDecodeError:
                return []
        log.log("Monsters loaded successfully", 2)

    def get_all_monsters(self):
        return self.monsters

    def get_monster_by_id(self, monster_id):
        for monster in self.monsters:
            if monster.id == monster_id:
                log.log(f"Monster found by id {monster_id}: {monster.name}", 2)
                return monster
        return None
class Monster:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.xp = data.get('xp')
        self.drop = data.get('drop', [])
        self.attack = data.get('attack')
        self.defense = data.get('defense')
        self.hp = data.get('hp')
        self.d_chance = data.get('d_chance')
        self.is_alive = True
        self.monsters = []
        self.monsters_path = 'resources/monsters.json'
        

    def load_monsters(self):
        if not os.path.exists(self.monsters_path):
            return []
        with open(self.weapons_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return [Monster(w) for w in data]
            except json.JSONDecodeError:
                return []
    def get_all_monsters(self):
        return self.monsters
    def get_monster_by_id(self, monster_id):
        for monster in self.monsters:
            if monster.id == monster_id:
                return monster
        return None
    
    # Getters and Setters
    def get_id(self):
        return self.id
    def set_id(self, id):
        self.id = id
    
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    
    def get_description(self):
        return self.description
    def set_description(self, description):
        self.description = description
    
    def get_xp(self):
        return self.xp
    def set_xp(self, xp):
        self.xp = xp
    
    def get_attack(self):
        return self.attack
    def set_attack(self, attack):
        self.attack = attack
    
    def get_defense(self):
        return self.defense
    def set_defense(self, defense):
        self.defense = defense
    
    def get_hp(self):
        return self.hp
    def set_hp(self, hp):
        self.hp = hp
    def reduce_hp(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
            self.is_alive = False
    
    def is_alive(self):
        if self.hp <= 0:
            return False, self.drop
        return self.hp > 0
    
    def get_drop(self):
        return self.drop
    
    def get_drop_by_id(self, drop_id):
        for drop in self.drop:
            if drop.id == drop_id:
                return drop
        return None
    

    def get_d_chance(self):
        return self.d_chance

    def drop_item(self):
        drop = []
        for id in self.drop:
            drop_rate = random.randint(0,100)
            if drop_rate <= self.get_d_chance(): #Zwroc ID dropu
                drop.append(id)
        return drop

    def __str__(self):
        log.log(f"Monster(id={self.id}\nname={self.name}\ndescription={self.description}\nxp={self.xp}\nattack={self.attack}\ndefense={self.defense}\nhp={self.hp})",2)
        return f"Monster(id={self.id}\nname={self.name}\ndescription={self.description}\nxp={self.xp}\nattack={self.attack}\ndefense={self.defense}\nhp={self.hp})"
