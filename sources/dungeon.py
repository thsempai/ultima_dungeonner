# -*- coding: utf-8 -*-
import cocos
import random

from db_connection import DBConnection
from server_connection import ServerConnection
from controler_manager import CONTROLER
from character import InventoryFull

TILESETS = {}
OBJECTS = {}
ENEMIES = {}

TILE_SIZE = 32,32


class Dungeon(list):

    def __init__(self,hero):
        self.hero = hero
        #uniquement pour les tests
        self.append(RoomScene(3,self.hero))

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
        CONTROLER.defineCommand('dungeon','grid_visibility',room.layer['grid'].switchVisibility)

    def changeRoom(self,index):

        self.__active_room = self[0]
        self.__mappingAction()

    def on_key_release(self,symbol, modifiers):

        CONTROLER.onKeyRelease('dungeon',symbol,modifiers)


class RoomScene(cocos.scene.Scene):

    def __init__(self, room_id,hero):

        cocos.scene.Scene.__init__(self)

        dungeon_size = 13,13
        self.size = dungeon_size

        entry = int(self.size[0]/2),0

        room_dict = DBConnection.getRoom(room_id)

        self.hero = None

        self.__name = room_dict['name']

        self.__events_queue = []

        self.__player_play = True

        self.__enemies_queue = []

        self.layer =    {
                        "room" : RoomLayer(room_dict['tileset'],self.size),
                        "item" : ItemLayer(room_dict['objects']),
                        "grid" : GridLayer(TILE_SIZE,self.size),
                        "character" : CharacterLayer(hero.image,entry,room_dict['enemies']),
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

        self.addHero(hero)

        self.schedule(self.__callback)

        self.layer['grid'].visible = False

    def addEvent(self,event):

        self.__events_queue.append(event) 

    def __repr__(self):

        return "RoomScene '" + self.__name +"'"

    def addHero(self,hero):
        self.hero = hero
        self.layer['gui'].refreshInventory(self.hero.inventory)

    def moveHero(self,move):

        CONTROLER.pause = True
        self.__player_play = False

        x,y =  self.layer['character'].getHeroPosition()
        x,y =  x +  move[0], y + move[1]

        if self.layer['room'].isPassable((x,y)):

            enemy =  self.layer['character'].getEnemy((x,y))

            if enemy != None:
                
                event = {
                        'type':'hero-attack',
                        'target': enemy
                        }

                self.addEvent(event)

                msg = str(self.hero) + ' attacks ' + str(event['target']) + '.'
                self.layer['gui'].addMessage(msg)

                self.layer['character'].heroAttack(move)

            else:
                self.layer['character'].moveHero(move)

            item = self.layer['item'].getItem((x,y))

            if item != None:
                
                if item.type == 'item':

                    event = {
                            'type': 'hero-find-item',
                            'item': item,
                            'position': (x,y)
                            }
                    self.addEvent(event)

            self.__initEnemiesTurn()

    def __initEnemiesTurn(self):

        self.__enemies_queue += self.layer['character'].getEnemies().keys()

    def __solveEvents(self):

        for event in self.__events_queue:

            if event['type'] == 'hero-attack':

                if self.hero.hp > 0:
                    dice = random.randint(1,20)

                    r = self.hero.thaco - dice

                    if r <= event['target'].ac:
                        #to touch

                        dgt = random.randint(1,6)
                        dgt -= event['target'].dr

                        if dgt > 0:

                            event['target'].hp -= dgt

                            msg = str(self.hero) + ' hurts ' + str(event['target']) + ' (' + str(dgt) +').'
                            self.layer['gui'].addMessage(msg)

                        else:

                            msg = str(event['target']) + ' blocks ' + str(self.hero) + ' attack.'
                            self.layer['gui'].addMessage(msg)

                    else:

                        msg = str(event['target']) + ' dodges ' + str(self.hero) + ' attack.'
                        self.layer['gui'].addMessage(msg)

            elif event['type'] == 'enemy-attack':

                if event['from'].hp > 0:

                    dice = random.randint(1,20)

                    r = event['from'].thaco - dice

                    if r <= self.hero.ac:
                        #to touch

                        dgt = random.randint(1,6)
                        dgt -= self.hero.dr

                        if dgt > 0:

                            self.hero.hp -= dgt

                            msg = str(event['from']) + ' hurts ' + str(self.hero) + ' (' + str(dgt) +').'
                            self.layer['gui'].addMessage(msg)

                        else:

                            msg = str(self.hero) + ' blocks ' + str(event['from']) + ' attack.'
                            self.layer['gui'].addMessage(msg)

                    else:

                        msg = str(self.hero) + ' dodges ' + str(event['from']) + ' attack.'
                        self.layer['gui'].addMessage(msg)

            elif event['type'] == 'hero-find-item':

                msg = msg = str(self.hero) + ' finds ' + str(event['item']) + '.'
                self.layer['gui'].addMessage(msg)

                try:
                    self.hero.addItem(event['item'])
                except InventoryFull:
                    msg = 'The inventory is full.'
                    self.layer['gui'].addMessage(msg)
                else:
                    self.layer['gui'].refreshInventory(self.hero.inventory)
                    self.layer['item'].removeItem(event['position'])

        self.__events_queue = []

    def __callback(self,dt):
        
        if not self.layer['character'].onAnimation():

            if self.__player_play:

                CONTROLER.pause = False
                self.__solveEvents()
                    
            else:
                self.__solveEvents()
                if(len(self.__enemies_queue)) > 0:
                    
                    ene_pos = self.__enemies_queue.pop(0)

                    event = self.layer['character'].moveEnemy(ene_pos)

                    if event != None:
                        if event['type'] == 'enemy-attack':
                            
                            msg = str(event['from']) + ' attacks ' + str(self.hero) + '.'

                            self.layer['gui'].addMessage(msg)
                            self.addEvent(event)

                else:

                    self.layer['character'].updateEnemiesPosition()
                    self.__player_play = True

            self.__checkDeads()

    def __checkDeads(self):

        for enemy in self.layer['character'].getEnemies().values():

            if enemy.hp <= 0:
                msg = str(enemy) + ' dies.'
                self.layer['gui'].addMessage(msg)
                self.layer['character'].kill(enemy)


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
        self.__inventory = []

        x = 485
        y = 120
        dy = 20

        for n in range(5):
            color = 100, 100, 100, 255
            if n == 0:
                color = 255, 255, 255, 255

            pos = x,y
            self.__labels.append(cocos.text.Label(position=pos,color=color))
            self.add(self.__labels[-1])
            y -= dy

        img = ServerConnection.getImage('img/gui/gui.png')
        gui = cocos.sprite.Sprite(img, position = (465,0), anchor=(0,0))
        self.add(gui)

    def addMessage(self, message):

        self.__messages.insert(0,message)
        self.__updateLabel()

    def __updateLabel(self):
        
        for index in range(min(5,len(self.__messages))):
            self.__labels[index].element.text = self.__messages[index]

    def refreshInventory(self,inventory):

        for item in self.__inventory:
            self.remove(item)

        self.__inventory = []

        position = 480,556
        dpos = 52,0

        for item in inventory:
            self.__inventory.append(item)
            item.position = position
            self.add(item)

            position = position[0] + dpos[0], position[1] + dpos[1]


class GridLayer(cocos.layer.Layer):

    def __init__(self,tilesize,size):
        
        cocos.layer.Layer.__init__(self)

        color = (255,50,50,150)

        for x in range(tilesize[0],(size[0]+2)*tilesize[0],tilesize[0]):
            line = cocos.draw.Line((x,tilesize[1]),(x,tilesize[1]*(size[1]+1)),color)
            self.add(line)

        for y in range(tilesize[1],(size[1]+2)*tilesize[1],tilesize[1]):
            line = cocos.draw.Line((tilesize[0],y),(tilesize[0]*(size[0]+1),y),color)
            self.add(line)

    def switchVisibility(self):

        self.visible = not self.visible


class ItemLayer(cocos.layer.Layer):

    def __init__(self,obj_dict):
        
        cocos.layer.Layer.__init__(self)
        self.__obj_dict = {}

        for pos,obj in obj_dict.items():

            name = obj['name']
            typ = obj['type']

            anchor = 0,0

            if typ == 'item':
                anchor = (0,TILE_SIZE[1]/-6)

            img = OBJECTS[name]

            sp = Sprite(name,typ,img,pos,anchor = anchor)

            self.__obj_dict[pos] = sp
            self.add(sp)

    def getItem(self,position):

        if position in self.__obj_dict:
            return self.__obj_dict[position] 

        return None

    def removeItem(self,position):
        item = self.__obj_dict.pop(position)
        self.remove(item)


class CharacterLayer(cocos.layer.Layer):

    def __init__(self, hero_image, hero_initial_position, ene_dict):

        cocos.layer.Layer.__init__(self)

        self.__hero_sprite = Sprite('hero','hero',hero_image,hero_initial_position,anchor=(0,TILE_SIZE[1]/-6))
        
        self.add(self.__hero_sprite)

        self.__ene_dict = {}


        for pos,enemy in ene_dict.items():

            name = enemy[0]
            lvl = enemy[1]

            ene = Enemy(name,lvl,pos)

            self.__ene_dict[pos] = ene
            self.add(ene)

    def kill(self,enemy):

        position = enemy.room_position
        self.__ene_dict.pop(position)
        self.remove(enemy)



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

    def getEnemies(self):

        return self.__ene_dict

    def moveHero(self, move):

        self.__hero_sprite.move(move)

    def heroAttack(self, direction):

        self.__hero_sprite.attack(direction)

    def updateEnemiesPosition(self):

        new_dict = {}

        for ene in self.__ene_dict.values():
            new_dict[ene.room_position] =  ene

        self.__ene_dict = new_dict

    def moveEnemy(self,position):

        if not self.__ene_dict.has_key(position):

            return None

        hero_position = self.__hero_sprite.room_position
        enemy =  self.__ene_dict[position]

        ex, ey = position
        hx, hy = hero_position

        dx = 0
        dy = 0

        if (hx - ex) > 0:
            dx = 1
        elif (hx - ex) < 0:
            dx = -1

        if (hy - ey) > 0:
            dy = 1
        elif (hy - ey) < 0:
            dy = -1

        pot = []

        if dx != 0:
            pot.append((dx,0))

        if dy != 0:
            pot.append((0,dy))

        l = []

        for index in range(len(pot)):
            x,y = pot[index]
            p = ex + x, ey + y

            if p == hero_position:
                l = [index]
                break

            if p not in [t.room_position for t in self.__ene_dict.values()]:
                l.append(index)

        if len(l) == 0:
            return

        move = pot[l[random.randint(0,len(l)-1)]]

        pos = ex + move[0], ey + move[1]

        if pos == hero_position:
            enemy.attack(move)

            event = {
                    'type':'enemy-attack',
                    'from': enemy
                    }
            return event

        else:
            enemy.move(move)

        return None


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

    def __init__(self,sprite,region,speed):

        image = sprite.image.get_region(*region)
        position = region[:2]

        self.Sprite(image,position=position,anchor=(0,0))
        self.__life = 2.
        self.__speed = speed
 
    
class Enemy(Sprite):

    def __init__(self,name,lvl,room_position):

        img = ENEMIES[name]
        anchor = (0,TILE_SIZE[1]/-6)

        self.__lvl = lvl

        Sprite.__init__(self,name,'enemy',img,room_position,anchor)

        self.thaco = 20
        self.ac = 10
        self.dr = 0
        self.__hp = [1,1]

    def __repr__(self):

        return Sprite.__repr__(self) + ' (lvl ' + str(self.__lvl) + ')'

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