from core.items import Items
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilities')))
from log_system import log

itemz_list = Items()
itemz_list.load_drop()

class Inventory:
    def __init__(self):
        self.items = []

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

eq = Inventory()