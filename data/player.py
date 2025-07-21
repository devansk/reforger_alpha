#Player class for a game
# - name
# - level
# - experience
# - balance
# -- attack
# -- defence
# -- critical hit chance

#@@IN-PROGRESS@@
# - saving system
# - eq system
# - inventory system
# - damage calculation

from core.inventory import Inventory
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilities')))
from log_system import log



class Player:
    @classmethod
    def load_from_file(cls, player_file='data/player_save.json', inventory_file='data/player_inventory.json'):
        import json, os
        # Wczytaj dane gracza
        if os.path.exists(player_file):
            with open(player_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {}
        # Wczytaj inventory
        from core.inventory import Inventory
        if os.path.exists(inventory_file):
            with open(inventory_file, 'r', encoding='utf-8') as f:
                inventory_data = json.load(f)
            inventory = Inventory.from_dict(inventory_data)
            # Zapamiętaj oryginalne itemy do późniejszego zapisu
            cls._loaded_inventory_items = list(inventory_data.get('items', []))
        else:
            inventory = Inventory()
            cls._loaded_inventory_items = []
        return cls(
            name=data.get('name', "Steve"),
            health=data.get('health', 100),
            level=data.get('level', 1),
            experience=data.get('experience', 0),
            experience_need=data.get('experience_need', 100),
            balance=data.get('balance', 0),
            attack=data.get('attack', 10),
            defense=data.get('defense', 5),
            critical_hit_chance=data.get('critical_hit_chance', 0.1),
            inventory=inventory
        )
    def save_to_file(self, filename='data/player_save.json'):
        import json, os
        data = {
            'name': self.name,
            'health': self.health,
            'health_max': self.health_max,
            'level': self.level,
            'experience': self.experience,
            'experience_need': self.experience_need,
            'balance': self.balance,
            'attack': self.attack,
            'defense': self.defense,
            'damage': self.damage,
            'critical_hit_chance': self.critical_hit_chance
            
        }
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Save inventory to a separate file, merging with previous items (no duplicates)
        inventory_file = 'data/player_inventory.json'
        os.makedirs(os.path.dirname(inventory_file), exist_ok=True)
        if hasattr(self.inventory, 'to_dict'):
            inventory_data = self.inventory.to_dict()
        elif hasattr(self.inventory, '__dict__'):
            inventory_data = self.inventory.__dict__
        else:
            inventory_data = str(self.inventory)

        prev_items = getattr(Player, '_loaded_inventory_items', [])
        new_items = inventory_data.get('items', [])
        # Merge by (id, name): sum quantity, max to m_quantity
        def get_key(item):
            if isinstance(item, dict):
                return (item.get('id'), item.get('name'))
            else:
                return (getattr(item, 'id', None), getattr(item, 'name', None))
        # Build dict: key -> item dict (with quantity)
        merged = {}
        for item in prev_items:
            key = get_key(item)
            if isinstance(item, dict):
                merged[key] = item.copy()
            else:
                merged[key] = item.__dict__.copy() if hasattr(item, '__dict__') else dict(item)
        for item in new_items:
            key = get_key(item)
            if key in merged:
                # sum quantity, but do not exceed m_quantity
                merged_item = merged[key]
                item_qty = item.get('quantity', 1) if isinstance(item, dict) else getattr(item, 'quantity', 1)
                max_qty = item.get('m_quantity', 1) if isinstance(item, dict) else getattr(item, 'm_quantity', 1)
                prev_qty = merged_item.get('quantity', 1)
                merged_item['quantity'] = min(prev_qty + item_qty, max_qty)
                merged_item['m_quantity'] = max_qty
            else:
                # add as dict
                merged[key] = item.copy() if isinstance(item, dict) else (item.__dict__.copy() if hasattr(item, '__dict__') else dict(item))
        combined = list(merged.values())
        with open(inventory_file, 'w', encoding='utf-8') as f:
            json.dump({'items': combined}, f, ensure_ascii=False, indent=4)
        # Update loaded inventory for next save
        Player._loaded_inventory_items = combined
        log.log(f"Player state saved to {filename} and inventory merged in {inventory_file}", 1)

    # def load_from_file(self, filename='data/player_save.json'):
    #     import json
    #     import os
    #     if not os.path.exists(filename):
    #         log.log(f"Save file {filename} not found.", 1)
    #         return
    #     with open(filename, 'r', encoding='utf-8') as f:
    #         data = json.load(f)
    #     self.name = data.get('name', self.name)
    #     self.health = data.get('health', self.health)
    #     self.health_max = data.get('health_max', self.health_max)
    #     self.level = data.get('level', self.level)
    #     self.experience = data.get('experience', self.experience)
    #     self.experience_need = data.get('experience_need', self.experience_need)
    #     self.balance = data.get('balance', self.balance)
    #     self.attack = data.get('attack', self.attack)
    #     self.defense = data.get('defense', self.defense)
    #     self.damage = data.get('damage', self.damage)
    #     self.critical_hit_chance = data.get('critical_hit_chance', self.critical_hit_chance)
    #     log.log(f"Player state loaded from {filename}", 1)
    def __init__(self, inventory=None, name="Steve", health=100, level=1, experience=0, experience_need=100, balance=0, attack=10, defense=5, critical_hit_chance=0.1):
        self.name = name
        self.health = health
        self.health_max = health  # Maximum health
        self.level = level
        self.experience = experience
        self.experience_need = experience_need if experience_need is not None else 100 * self.level  # Experience needed for next level
        self.balance = balance
        self.inventory = inventory if inventory is not None else Inventory()
        self.attack = attack
        self.defense = defense
        self.damage = int(self.attack * 0.75)
        self.critical_hit_chance = critical_hit_chance
        # log.log(f"Player {self.name} created with {self.health} health, level {self.level}, and {self.balance} balance.", 1)

    def __str__(self):
        return f"Name: {self.name}\nLevel: {self.level}\nExperience: {self.experience}/{self.experience_need}\nMoney: {self.balance}\nHealth: {self.health}/{self.health_max}\nAttack: {self.attack}\nDefense: {self.defense}\nDamage: {self.damage}"
#NAME
    #update:
    def get_name(self):
        return self.name
    def set_name(self, name):
        name = input("Enter your name: ")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if len(name) > 20:
            raise ValueError("Name must be 20 characters or less.")
        if not name.isalnum():
            raise ValueError("Name must contain only alphanumeric characters.")
        if name.lower() == "admin":
            raise ValueError("Name cannot be 'admin'.")
        
        self.name = name
#DAMAGE
    #update:
    def get_damage(self):
        return self.damage
#HEALTH
    #update:
    def get_health(self):
        return self.health
    def add_health(self, amount):
        self.health += amount
    def set_health(self, health):
        self.health = health
    def reduce_health(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0
#HEALTH MAX
    #update:
    def get_health_max(self):
        return self.health_max
    def set_health_max(self, health_max):
        self.health_max = health_max
    def add_health_max(self, amount):
        self.health_max += amount
    def reduce_health_max(self, amount):
        self.health_max -= amount
        if self.health_max < 1:
            self.health_max = 1
        if self.health > self.health_max:
            self.health = self.health_max

#LEVEL
    #update: - this section is updated to include health max increase on level up
    def get_level(self):
        return self.level
    def add_level(self, levels=1):
        self.level += levels
    def set_level(self, level):
        self.level = level
    def reduce_level(self, levels=1):
        self.level -= levels
        if self.level < 1:
            self.level = 1
    def level_up(self):

        self.add_level()
        log.log(f"{self.name} leveled up to level {self.level}!", 1)
        self.set_experience(0)  # Reset experience on level up
        self.add_experience_need(100)  # Increase experience need for next level
        log.log(f"{self.name} needs {self.experience_need} experience for the next level.", 1)
        self.add_health_max(10*self.get_level())  # Increase max health on level up
        log.log(f"{self.name}'s max health increased to {self.health_max}.", 1)
        self.set_health(self.health_max)  # Restore health to max on level up
        log.log(f"{self.name}'s health restored to max ({self.health}).", 1)

#EXPERIENCE
    #update:
    def get_experience(self):
        return self.experience
    def add_experience(self, exp):
        self.experience += exp
        if self.experience > self.experience_need:
            xp = self.experience - self.experience_need
            self.level_up()
            self.add_experience(xp)  # Add excess experience to next level           
    def set_experience(self, exp):
        self.experience = exp
    def reduce_experience(self, exp):
        self.experience -= exp
        if self.experience < 0:
            self.experience = 0
#EXPERIENCE NEED
    #update:
    def get_experience_need(self):
        return self.experience_need
    def set_experience_need(self, exp_need):
        self.experience_need = exp_need
    def add_experience_need(self, amount):
        self.experience_need += amount
    def reduce_experience_need(self, amount):
        self.experience_need -= amount
        if self.experience_need < 0:
            self.experience_need = 0

#BALANCE
    #update:
    def get_balance(self):
        return self.balance        
    def add_balance(self, amount):
        self.balance += amount
    def set_balance(self, amount):
        self.balance = amount
    def reduce_balance(self, amount):
        self.balance -= amount
        if self.balance < 0:
            self.balance = 0

#ATTACK
    #update:
    def get_attack(self):
        return self.attack
    def add_attack(self, amount):
        self.attack += amount
    def set_attack(self, attack):
        self.attack = attack
    def reduce_attack(self, amount):
        self.attack -= amount
        if self.attack < 0:
            self.attack = 1
#CRITICAL HIT CHANCE
    #update:
    def get_critical_hit_chance(self):
        return self.critical_hit_chance
    def set_critical_hit_chance(self, chance):
        self.critical_hit_chance = chance
    def add_critical_hit_chance(self, amount):
        self.critical_hit_chance += amount
    def reduce_critical_hit_chance(self, amount):
        self.critical_hit_chance -= amount
        if self.critical_hit_chance < 0:
            self.critical_hit_chance = 0.1

#DEFENSE
    #update:
    def get_defense(self):
        return self.defense
    def add_defense(self, amount):
        self.defense += amount
    def set_defense(self, defense):
        self.defense = defense
    def reduce_defense(self, amount):
        self.defense -= amount
        if self.defense < 0:
            self.defense = 0

#INVENTORY
    #update:
    def get_inventory(self):
        return self.inventory
    def add_inventory(self,item_id,item_get):
        self.inventory.add_item(item_id,item_get)
    
    
   
        