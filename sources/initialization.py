
import cocos
import pyglet
import getpass

from db_connection import DBConnection
from server_connection import ServerConnection

from data import TILESETS, OBJECTS, ENEMIES, TEXTS, TILE_SIZE

from dungeon import Dungeon, RoomScene
from db_connection import DBConnection
from server_connection import ServerConnection
from user import User
from menu import MainMenu, MENU_TRANSITION
from another_scene import creditsScene
from ud_exception import UDungeonException

from data import SCREEN_SIZE, TITLE

fonts = ['drakoheart.ttf']

def play(scene):
    
    scene = MENU_TRANSITION(scene)
    cocos.director.director.push(scene)

class InitLayer(cocos.scene.Scene):

    def __init__(self,w_game):

        cocos.scene.Scene.__init__(self)

        text = 'Loading ... 0%'

        self.label = cocos.text.Label(text,position = (400,300), font_name = 'Drakoheart Leiend', font_size = 40, anchor_x = 'center')
        self.add(self.label)
        self.schedule(self.__callback)
        self.loading = init()
        self.__time = 2.
        self.w_game = w_game

    def getMain(self):

        user = DBConnection.getUser(getpass.getuser())

        user = User(user)
        hero = user.getHero()

        dungeon = Dungeon(hero)
        self.w_game.push_handlers(dungeon)
        
        credits_scene = creditsScene()


        #main scene

        main_command =  [
                        ('Play',play,[dungeon[0]]),
                        ('Credits',play,[credits_scene]),
                        ('Quit',self.w_game.close,[])
                        ]

        main_scene =  cocos.scene.Scene()
        menu =  MainMenu(main_command)

        #Title
        label = cocos.text.Label(TITLE,position = (400,500), font_name = 'Drakoheart Leiend', font_size = 45, anchor_x = 'center')
        main_scene.add(label)

        main_scene.add(menu)

        #music
        bgm = ServerConnection.getMusic('bgm/main_screen.ogg')
        bgm_player = pyglet.media.Player()
        bgm_player.queue(bgm)
        bgm_player.eos_action = bgm_player.EOS_LOOP
        bgm_player.play()

        return main_scene
       

    def __callback(self,dt):

        try:
            if self.loading == None:
                self.__time -= dt
                if self.__time <= 0.:
                    main_scene = self.getMain()
                    cocos.director.director.replace(main_scene)
                    return
                else:
                    return

            pc = self.loading.next()
            self.label.element.text = 'Loading ... ' + str(int(pc*100)) + '%'

        except StopIteration as e:
            self.loading = None

def init():


    def step(s):
        n_step = 7.
        pc =s/n_step
        return round(pc,2)
    
    ServerConnection.createDirectories()
    yield step(1)

    loadTileset()
    yield step(2)

    loadObjects()
    yield step(3)

    loadEnemies()
    yield step(4)

    loadFonts()
    yield step(5)

    main_directory = ServerConnection.getMainDirectory()
    pyglet.resource.path.append(main_directory + '/bgm')
    pyglet.resource.reindex()
    yield step(6)

    ServerConnection.getClientPath('img/gui/gui.png')
    ServerConnection.getClientPath('bgm/main_screen.ogg')
    yield step(7)


def getTile(img,pos):
    return img.get_region(pos[0]*TILE_SIZE[0],pos[1]*TILE_SIZE[1],TILE_SIZE[0],TILE_SIZE[1])


def loadTileset():

    dic = {}

    sql =  "select til_name, til_path, til_type "
    sql += "from tileset "

    rows = DBConnection.getResult(sql)

    tiles =     {   'wall-nw':      (0,3),
                    'wall-n':       (1,3),
                    'wall-ne':      (2,3),
                    'wall-w':       (0,2),
                    'wall-e':       (2,2),
                    'wall-sw':      (0,1),
                    'wall-s':       (1,1),
                    'wall-se':      (2,1),
                    'door-n':       (3,3),
                    'door-s':       (3,2),
                    'ground':       (1,2),
                    'ground-alt1':  (0,0),
                    'ground-alt2':  (1,0),
                    'ground-alt3':  (2,0),
                    'empty':        (3,0)
                }

    for row in rows:

        name = row[0]
        path = row[1]
        type_tileset = row[2]

        if type_tileset == 'room':
            img = ServerConnection.getImage(path)

            tileset = cocos.tiles.TileSet(name, None)
            for n, p in tiles.items():
                prop =  {   'passable': True,
                            'transition' : False
                        }

                if n == 'door-n':
                    prop['transition'] = True

                tileset.add( prop, getTile(img,p), n)
                dic[name] = tileset
        else:
            ServerConnection.getClientPath(path)

    global TILESETS
    TILESETS.update(dic)

def loadObjects():

    sql =  "select obj_name, obj_description, til_path, obj_til_x, obj_til_y "
    sql += "from object "
    sql += "inner join tileset on obj_til_xid = til_id ";

    rows = DBConnection.getResult(sql)

    dic = {}
    text = {}

    for obj in rows:
        name = obj[0]
        decription = obj[1]
        region = obj[3] * TILE_SIZE[0], obj[4] * TILE_SIZE[0], TILE_SIZE[0], TILE_SIZE[1]
        path = obj[2]

        img = ServerConnection.getImage(path,region)

        text[name]= decription
        dic[name] = img

    global OBJECTS
    global TEXTS

    OBJECTS.update(dic)
    TEXTS['object'].update(text)

def loadEnemies():

    sql =  "select ene_name, ene_description, til_path, ene_til_x, ene_til_y "
    sql += "from enemy "
    sql += "inner join tileset on ene_til_xid = til_id ";

    rows = DBConnection.getResult(sql)

    dic = {}
    text = {}

    for ene in rows:
        name = ene[0]
        decription = ene[1]
        region = ene[3] * TILE_SIZE[0], ene[4] * TILE_SIZE[0], TILE_SIZE[0], TILE_SIZE[1]
        path = ene[2]

        img = ServerConnection.getImage(path,region)

        dic[name] = img
        text[name]= decription

    global ENEMIES
    global TEXTS


    ENEMIES.update(dic)
    TEXTS['enemy'].update(text)

def loadFonts():
    main_directory = ServerConnection.getMainDirectory()

    pyglet.resource.path.append(main_directory + '/fonts')
    pyglet.resource.reindex()

    for font in fonts:
        ServerConnection.getClientPath('fonts/'+font)
        pyglet.resource.add_font(font)