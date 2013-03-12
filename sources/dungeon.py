# -*- coding: utf-8 -*-
import cocos
import random

from db_connection import DBConnection
from controler_manager import CONTROLER

TILESETS = {}
OBJECTS = {}
ENEMIES = {}

TILE_SIZE = 32,32


class Dungeon(list):

    def __init__(self,hero):
        self.hero = hero
        #uniquement pour les tests
        self.append(RoomScene(3,self.hero.image))

        self.__active_room = None

        self.changeRoom(0)


    def __repr__(self):

        return "Class Dungeon"

    def __mappingAction(self):

        room = self.__active_room

        CONTROLER.defineCommand('dungeon','hero_up',room.moveHero,[(0,1)])
        CONTROLER.defineCommand('dungeon','hero_down',room.moveHero,[(0,-1)])
        CONTROLER.defineCommand('dungeon','hero_left',room.moveHero,[(-1,0)])
        CONTROLER.defineCommand('dungeon','hero_right',room.moveHero,[(1,0)])

    def changeRoom(self,index):

        self.__active_room = self[0]
        self.__mappingAction()

    def on_key_release(self,symbol, modifiers):
        CONTROLER.onKeyRelease('dungeon',symbol,modifiers)


class RoomScene(cocos.scene.Scene):

    def __init__(self, room_id,hero_image):

        cocos.scene.Scene.__init__(self)

        dungeon_size = 13,13
        self.size = dungeon_size

        entry = int(self.size[0]/2),0

        room_dict = DBConnection.getRoom(room_id)

        self.__name = room_dict['name']

        self.__events_queue = []

        self.layer =    {
                        "room" : RoomLayer(room_dict['tileset'],self.size),
                        "item" : ItemLayer(room_dict['objects']),
                        "grid" : GridLayer(TILE_SIZE,self.size),
                        "character" : CharacterLayer(hero_image,entry,room_dict['enemies']),
                        "gui" : GUILayer()
                        }
        z = {
            "room" : 0,
            "grid" : 1,
            "item" : 2,
            "character" : 3,
            "gui" : 4
            }

        for key, value in self.layer.items():
            self.add(value,z=z[key])

        self.schedule(self.__callback)


    def __addEvent(self,event):
        self.__events_queue.append(event) 

    def __repr__(self):

        return "RoomScene '" + self.__name +"'"

    def moveHero(self,move):
        CONTROLER.pause = True
        x,y =  self.layer['character'].getHeroPosition()
        x,y =  x +  move[0], y + move[1]

        if self.layer['room'].isPassable((x,y)):

            enemy =  self.layer['character'].getEnemy((x,y))

            if enemy != None:
                
                event = {
                        'type':'hero-attack',
                        'target': enemy
                        }

                self.__addEvent(event)

                msg = 'Hero attacks ' + str(event['target'])
                self.layer['gui'].addMessage(msg)

                self.layer['character'].heroAttack(move)

            else:
                self.layer['character'].moveHero(move)

    def __solveEvents(self):
        for event in self.__events_queue:
            if event['type'] == 'hero-attack':

                msg = 'Hero hurts ' + str(event['target'])
                self.layer['gui'].addMessage(msg)

        self.__events_queue = []

    def __callback(self,dt):
        
        if not self.layer['character'].onAnimation():
            CONTROLER.pause = False
            if len(self.__events_queue) > 0:
                self.__solveEvents()


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

    def _isValid(self,position):

        x,y = position

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

class GUILayer(cocos.layer.Layer):

    def __init__(self):
        cocos.layer.Layer.__init__(self)

        self.__messages = []
        self.__labels = []

        x = 500
        y = 120
        dy = 20 

        for n in range(5):
            pos = x,y
            self.__labels.append(cocos.text.Label(position=pos))
            self.add(self.__labels[-1])
            y -= dy

    def addMessage(self, message):

        self.__messages.insert(0,message)
        self.__updateLabel()

    def __updateLabel(self):
        
        for index in range(min(5,len(self.__messages))):
            self.__labels[index].element.text = self.__messages[index]


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

    def __init__(self, hero_image, hero_initial_position, ene_dict):

        cocos.layer.Layer.__init__(self)

        self.__hero_sprite = Sprite(hero_image,hero_initial_position,anchor=(0,TILE_SIZE[1]/-6))
        
        self.add(self.__hero_sprite)

        self.__ene_dict = {}

        for pos,enemy in ene_dict.items():
            name = enemy[0]
            lvl = enemy[1]

            ene = Enemy(name,lvl,pos)

            self.__ene_dict[pos] = ene
            self.add(ene)

    
    def onAnimation(self):
        if self.__hero_sprite.are_actions_running():
            return True

        for enemy in self.__ene_dict.values():
            if enemy.are_actions_running():
                return True

        return False

    def getHeroPosition(self):

        return self.__hero_sprite.room_position

    def getEnemy(self, position):

        if position in self.__ene_dict:
            return self.__ene_dict[position]

        return None

    def moveHero(self, move):

        self.__hero_sprite.move(move)

    def heroAttack(self,direction):

        self.__hero_sprite.attack(direction)


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

    def attack(self,direction):

        move = direction[0]*0.5, direction[1] *0.5
        move = MoveTile(move,duration=0.25)
        rmove = cocos.actions.base_actions.Reverse(move)
        self.do(move + rmove)


    def move(self,move):

        self.do(MoveTile(move))

    
class Enemy(Sprite):

    def __init__(self,name,lvl,room_position):

        img = ENEMIES[name]
        anchor = (0,TILE_SIZE[1]/-6)

        self.__name = name
        self.__lvl = lvl

        Sprite.__init__(self,img,room_position,anchor)


    def __repr__(self):

        return self.__name + ' (lvl ' + str(self.__lvl) + ')'


class MoveTile(cocos.actions.interval_actions.MoveBy):

    def __init__(self,(dx,dy),duration=0.5):
        delta = dx*TILE_SIZE[0], dy*TILE_SIZE[1]

        cocos.actions.interval_actions.MoveBy.__init__(self,delta,duration)