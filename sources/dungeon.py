# -*- coding: utf-8 -*-
import cocos
#import fait pour contrer un bug(?)
import cocos.scenes

import random

from data import TILESETS, DUNGEON_SIZE,TILE_SIZE
from db_connection import DBConnection

# -- CONSTANTE TECHNIQUE --

N_TILE = 12


class Dungeon:

    def __init__(self,hero):

        self.rooms = []

        rooms = DBConnection.getDungeon(3)

        for room_id in rooms:
            self.rooms.append(Room(room_id))
        


class Room(cocos.scene.Scene):

    def __init__(self,room_id):

        cocos.scene.Scene.__init__(self)

        self.room_data =  DBConnection.getRoom(room_id)
        self.layer = {}

        self.build()


    def build(self):

        self.layer['room'] = RoomLayer(self.room_data['tileset'],DUNGEON_SIZE)
        self.add(self.layer['room'], z=0)

        


class RoomLayer(cocos.tiles.RectMapLayer):

    def __init__(self, tileset, size):

        self.size = size
        self.tileset = TILESETS[tileset]

        self.__build()
        self.__applyTiles()

        cocos.tiles.RectMapLayer.__init__(self,'room',self.size[0],self.size[1],self.cells)
        self.set_view(0,0,N_TILE*8,N_TILE*8)  

    def __build(self):
        self.cells = []

        for x in range(self.size[0]+2):
            line = []
            for y in range(self.size[1]+2):
                tile = 'ground'
                if x == 0:
                    if y == 0:
                        tile = 'wall-sw'
                    elif y == self.size[1]+1:
                        tile = 'wall-nw'
                    else:
                        tile = 'wall-w'
                elif x == self.size[0]/2 +1:
                    if y == self.size[1]+1:
                        tile = 'door-n'
                    elif y == 0:
                        tile = 'door-s'
                elif x == self.size[0]+1:
                    if y == 0:
                        tile = 'wall-se'
                    elif y == self.size[1]+1:
                        tile = 'wall-ne'
                    else:
                        tile = 'wall-e'
                elif y == 0:
                        tile = 'wall-s'
                elif y == self.size[1]+1:
                    tile = 'wall-n'
                if tile == 'ground':
                    if random.randint(0,100) > 75:
                        tile = 'ground-alt' + str(random.randint(1,3))

                line.append(tile)
            self.cells.append(line)

    def __applyTiles(self):

        for x in range(self.size[0]+2):
            for y in range(self.size[1]+2):
                self.cells[x][y] = cocos.tiles.RectCell(x,y,TILE_SIZE[0],TILE_SIZE[1],{},self.tileset[self.cells[x][y]])

    def _isValid(self,position):

        x,y = position
        
        #entrée
        if x == 6 and y == 13:
            return True

        if x < 0 or x >= self.size[0]:
            return False

        if y < 0 or y >= self.size[1]:
            return False

        return True

    def isPassable(self, position):
        
        x,y = position
        
        if self._isValid(position):

            return self.get_cell(x,y)['passable']

        return False

    def isTransition(self,(x,y)):
        #à corriger
        if x == 6 and y == 13:
            return True

        return self.get_cell(x,y)['transition']