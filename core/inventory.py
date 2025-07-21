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
    def add_item(self, item_id, item_get):
        # Pobierz przedmiot z odpowiedniej listy
        if item_get == 'weapon':
            przedmiot = itemz_list.get_weapon_by_id(item_id)
        elif item_get == 'shield':
            przedmiot = itemz_list.get_shield_by_id(item_id)
        elif item_get == 'potion':
            przedmiot = itemz_list.get_potion_by_id(item_id)
        elif item_get == 'drop':
            przedmiot = itemz_list.get_drop_by_id(item_id)
        else:
            log.log(f"Unknown item type: {item_get}", 4)
            return
        if not przedmiot:
            log.log(f"Item with id {item_id} not found in {item_get}s", 4)
            return

        # Jeśli już jest w inventory, zwiększ quantity
        for item in self.items:
            item_id_val = item['id'] if isinstance(item, dict) else item.id
            if item_id_val == przedmiot.id:
                # obsłuż quantity/m_quantity dla dict i obiektu
                if isinstance(item, dict):
                    if item['quantity'] < item['m_quantity']:
                        item['quantity'] += 1
                        log.log(f"{item['name']} quantity increased to {item['quantity']}/{item['m_quantity']}", 4)
                    else:
                        log.log(f"Cannot add {item['name']}, max quantity reached", 4)
                else:
                    if item.quantity < item.m_quantity:
                        item.quantity += 1
                        log.log(f"{item.name} quantity increased to {item.quantity}/{item.m_quantity}", 4)
                    else:
                        log.log(f"Cannot add {item.name}, max quantity reached", 4)
                return
        # Jeśli nie ma, dodaj z quantity=1
        przedmiot.quantity = 1
        log.log(f"{przedmiot.name} added to inventory", 4)
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