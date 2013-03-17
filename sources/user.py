# -*- coding: utf-8 -*-

from character import Hero

class User:

    def __init__(self,data):

        self.name = data['name']

    def getHero(self):

        hero = Hero(self.name)
        return hero