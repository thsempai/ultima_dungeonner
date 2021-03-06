# -*- coding: utf-8 -*-
from server_connection import ServerConnection


## constants ##
from data import N_ITEM, ITEM_PROPERTY


class InventoryFull(Exception):
    def __init__(self):
        self.message = 'InventoryFull'


class Hero(object):

    def __init__(self,name):

        self.image = ServerConnection.getImage('img/tileset/hero.png')
        self.name =  name.capitalize()

        self.inventory = []

        self.__thaco = 20
        self.__ac = 10
        self.__dr = 0
        self.__hp = [20,20]

    def __repr__(self):

        return self.name

    def getLife(self):

        return self.__hp

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


    def hp():
       
        #doc
        doc = "healt point"
        
        #getter
        def fget(self):

            hp = self.__hp[0]

            return self.__hp[0]
        
        #setter
        def fset(self, hp):

            self.__hp[0] = max(0,min(hp, self.__hp[1]))
        
        #deleter
        def fdel(self):
            pass

        return locals()

    hp = property(**hp())


    def addItem(self,item):
        if len(self.inventory) > N_ITEM:
            raise InventoryFull
        
        self.inventory.append(item)

    def useItem(self, index):

        if index >= N_ITEM:
            return

        item = self.inventory[index]
        name = str(item)

        prop = ITEM_PROPERTY[name]

        for key,action in prop.items():
            if key == 'healing':
                self.hp += action

        self.inventory.pop(index)






