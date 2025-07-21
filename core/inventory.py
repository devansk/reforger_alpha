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
        if item_get == 'drop':
            self.items.append(itemz_list.get_drop_by_id(item_id))
            log.log(f"{itemz_list.get_drop_by_id(item_id)} added to inventory",1)

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