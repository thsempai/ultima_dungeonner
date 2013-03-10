# -*- coding: utf-8 -*-
import cocos
import random

from db_connection import DBConnection

TILESETS = {}
OBJECTS = {}

TILE_SIZE = 32,32



class Dungeon(list):

    def __init__(self,hero):
        self.hero = hero
        #uniquement pour les tests
        self.append(RoomScene(2,self.hero.image))

    def __repr__(self):

        return "Class Dungeon"


class RoomScene(cocos.scene.Scene):

    def __init__(self, room_id,hero_image):

        cocos.scene.Scene.__init__(self)

        dungeon_size = 13,13
        self.size = dungeon_size

        entry = int(self.size[0]/2),0

        room_dict = DBConnection.getRoom(room_id)

        self.__name = room_dict['name']

        self.layer =    {
                        "room" : RoomLayer(room_dict['tileset'],self.size),
                        "item" : ItemLayer(room_dict['objects']),
                        "grid" : GridLayer(TILE_SIZE,self.size),
                        "character" : CharacterLayer(hero_image,entry)
                        }
        z = {
            "room" : 0,
            "grid" : 1,
            "item" : 2,
            "character" : 3
            }

        for key, value in self.layer.items():
            self.add(value,z=z[key])


    def __repr__(self):

        return "RoomScene '" + self.__name +"'"


class RoomLayer(cocos.tiles.RectMapLayer):

    def __init__(self, tileset, size):

        self.size = size
        self.tileset = TILESETS[tileset]

        self.__build()
        self.__applyTiles()

        cocos.tiles.RectMapLayer.__init__(self,'room',self.size[0],self.size[1],self.cells)
        self.set_view(0,0,self.size[0]*TILE_SIZE[0], self.size[1]*TILE_SIZE[0])
        

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

class GridLayer(cocos.layer.Layer):

    def __init__(self,tilesize,size):
        
        cocos.layer.Layer.__init__(self)

        color = (150,255,150,125)

        for x in range(0,(size[0]+3)*tilesize[0],tilesize[0]):
            line = cocos.draw.Line((x,0),(x,tilesize[1]*(size[1]+2)),color)
            self.add(line)

        for y in range(0,(size[1]+3)*tilesize[1],tilesize[1]):
            line = cocos.draw.Line((0,y),(tilesize[0]*(size[0]+2),y),color)
            self.add(line)



class ItemLayer(cocos.layer.Layer):

    def __init__(self,obj_dict):
        
        cocos.layer.Layer.__init__(self)
        self.__obj_dict = {}

        for pos,name in obj_dict.items():

            img = OBJECTS[name]
            sp = Sprite(img,pos)

            self.__obj_dict[pos] = sp
            self.add(sp)

class CharacterLayer(cocos.layer.Layer):

    def __init__(self, hero_image, hero_initial_position):
        cocos.layer.Layer.__init__(self)

        self.hero_tile_position = hero_initial_position
        self.__hero_sprite = Sprite(hero_image,hero_initial_position,anchor=(0,TILE_SIZE[1]/-6))
        
        self.add(self.__hero_sprite)

class Sprite(cocos.sprite.Sprite):

    def __init__(self,image,room_position,anchor=(0,0)):

        cocos.sprite.Sprite.__init__(self,image,anchor=anchor)
        self.room_position = room_position

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

    

