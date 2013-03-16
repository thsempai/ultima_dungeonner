# -*- coding: utf-8 -*-
from server_connection import ServerConnection
import getpass

class InventoryFull(Exception):
    def __init__(self):
        self.message = 'InventoryFull'


class Hero:

    def __init__(self):

        self.image = ServerConnection.getImage('img/tileset/hero.png')
        self.name =  getpass.getuser().capitalize()

        self.inventory = []

        self.__thaco = 20
        self.__ac = 10
        self.__dr = 0

        self.hp = [10,10]

    def thaco():
       
        #doc
        doc = "To Hit AC 0"
        
        #getter
        def fget(self):

            #gestion du matériel ici
            thaco = self.__thaco

            return thaco
        
        #setter
        def fset(self, thaco):

            self.__thaco = thaco
        
        #deleter
        def fdel(self):
            pass

        return locals()

    thaco = property(**thaco())

    def ac():
       
        #doc
        doc = "Armor Class"
        
        #getter
        def fget(self):

            #gestion du matériel ici
            ac = self.__ac

            return ac
        
        #setter
        def fset(self, ac):

            self.__ac = ac
        
        #deleter
        def fdel(self):
            pass

        return locals()

    ac = property(**ac())

    def dr():
       
        #doc
        doc = "deguat reduction"
        
        #getter
        def fget(self):

            #gestion du matériel ici
            dr = self.__dr

            return dr
        
        #setter
        def fset(self, dr):

            self.__dr = dr
        
        #deleter
        def fdel(self):
            pass

        return locals()

    dr = property(**dr())


    def addItem(self,item):
        if len(self.inventory) > 3:
            raise InventoryFull

        self.inventory.append(item)

