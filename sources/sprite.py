# -*- coding: utf-8 -*-

import cocos

from data import TILE_SIZE, ENEMIES

class Sprite(cocos.sprite.Sprite):

    def __init__(self,name,typ,image,room_position,anchor=(0,0)):

        cocos.sprite.Sprite.__init__(self,image,anchor=anchor)
        self.room_position = room_position
        self._name = name
        self.type = typ

    def __repr__(self):

        return self._name

    def room_position():
       
        #doc
        doc = "position du sprite dans la room"
        
        #getter
        def fget(self):

            pos = self.position
            pos = pos[0] - TILE_SIZE[0], pos[1] - TILE_SIZE[1]
            pos = int(pos[0] / TILE_SIZE[0]), int(pos[1] / TILE_SIZE[1])

            return pos
        
        #setter
        def fset(self, pos):

            pos = int(pos[0]*TILE_SIZE[0]), int(pos[1]*TILE_SIZE[1])
            pos = pos[0] + TILE_SIZE[0], pos[1] + TILE_SIZE[1]
            self.position = pos
        
        #deleter
        def fdel(self):
            pass

        return locals()

    room_position = property(**room_position())

    def attack(self,direction):

        move = direction[0]*0.5, direction[1] *0.5
        move = MoveTile(move,duration=0.25)
        rmove = cocos.actions.base_actions.Reverse(move)
        self.do(move + rmove)

    def move(self,move):

        self.do(MoveTile(move))


class Particle(cocos.sprite.Sprite):

    def __init__(self,sprite,region,anchor=(0,0)):

        image = sprite.image.get_region(*region)

        position = region[:2]
        position = -1 * anchor[0] + position[0], -1* anchor[1] + position[1]
        position = sprite.position[0] + position[0], sprite.position[1] + position[1]  

        cocos.sprite.Sprite.__init__(self,image,position=position,anchor=(0,0))
        self.life = 1.

        self.schedule(self.__callback)

    def __callback(self,dt):

        self.life -= dt

        if self.life <= 0.:
            self.kill()
 

class Enemy(Sprite):

    def __init__(self,name,lvl,room_position):

        img = ENEMIES[name]
        anchor = (0,TILE_SIZE[1]/-6)

        self.__lvl = lvl

        Sprite.__init__(self,name,'enemy',img,room_position,anchor)

        self.thaco = 20
        self.ac = 20
        self.dr = 0
        self.__hp = [5,5]

    def getLife(self):
        return self.__hp

    def hp():
       
        #doc
        doc = "healt point"
        
        #getter
        def fget(self):

            hp = self.__hp[0]

            return self.__hp[0]
        
        #setter
        def fset(self, hp):

            self.__hp[0] = min(hp, self.__hp[1])
        
        #deleter
        def fdel(self):
            pass

        return locals()

    hp = property(**hp())


class MoveTile(cocos.actions.interval_actions.MoveBy):

    def __init__(self,(dx,dy),duration=0.5):
        delta = dx*TILE_SIZE[0], dy*TILE_SIZE[1]

        cocos.actions.interval_actions.MoveBy.__init__(self,delta,duration)