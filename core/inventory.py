    # @classmethod
    # def from_dict(cls, data):
    #     obj = cls()
    #     for key, value in data.items():
    #         setattr(obj, key, value)
    #     return obj
from core.items import Items
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilities')))
from log_system import log

itemz_list = Items()
itemz_list.load_drop()

class Inventory:
    @classmethod
    def from_dict(cls, data):
        obj = cls()
        for key, value in data.items():
            setattr(obj, key, value)
        return obj
    def __init__(self):
        self.items = []

#jeśli item_po_id jest w eq to dodaj quantity danego itema, max 32
#dodać max quantity do itemów
    def add_item(self, item_id,item_get):

        if item_get == 'weapon':
            if not itemz_list.get_weapon_by_id(item_id):
                log.log(f"Item with id {item_id} not found in weapons", 4)
                return
            else:
                przedmiot = itemz_list.get_weapon_by_id(item_id)
        elif item_get == 'shield':
            if not itemz_list.get_shield_by_id(item_id):
                log.log(f"Item with id {item_id} not found in shields", 4)
                return
            else:
                przedmiot = itemz_list.get_shield_by_id(item_id)
        elif item_get == 'potion':
            if not itemz_list.get_potion_by_id(item_id):
                log.log(f"Item with id {item_id} not found in potions", 4)
                return
            else:
                przedmiot = itemz_list.get_potion_by_id(item_id)
        elif item_get == 'drop':
            if not itemz_list.get_drop_by_id(item_id):
                log.log(f"Item with id {item_id} not found in drops", 4)
                return
            else:
                przedmiot = itemz_list.get_drop_by_id(item_id)
        

        for item in self.items:
            if item.id == przedmiot.id: #jesli przedmiot w inventory zwieksz ilosc
                if item.quantity < item.m_quantity:
                    item.quantity += 1
                    log.log(f"{item.name} quantity increased to {item.quantity}/{item.m_quantity}", 4)
                    return
                else:
                    log.log(f"Cannot add {item.name}, max quantity reached", 4)
                    return
        
        log.log(f"{przedmiot.name} added to inventory", 4)
        przedmiot.quantity = 1
        self.items.append(przedmiot)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def list_items(self):
        return self.items

    def clear_inventory(self):
        self.items.clear()

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                result[key] = []
                for item in value:
                    if hasattr(item, 'to_dict'):
                        result[key].append(item.to_dict())
                    elif hasattr(item, '__dict__'):
                        result[key].append(item.__dict__)
                    else:
                        result[key].append(item)
            elif hasattr(value, 'to_dict'):
                result[key] = value.to_dict()
            elif hasattr(value, '__dict__'):
                result[key] = value.__dict__
            else:
                result[key] = value
        return result

eq = Inventory()