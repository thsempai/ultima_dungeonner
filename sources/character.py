# -*- coding: utf-8 -*-
from server_connection import ServerConnection

class InventoryFull(Exception):
    def __init__(self):
        self.message = 'InventoryFull'


class Hero:

    def __init__(self):

        self.image = ServerConnection.getImage('img/tileset/hero.png')
        self.name = 'MySelf'

        self.inventory = []

    def addItem(self,item):
        if len(self.inventory) > 3:
            raise InventoryFull

        self.inventory.append(item)

