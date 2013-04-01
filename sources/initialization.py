
import cocos
import pyglet

from db_connection import DBConnection
from server_connection import ServerConnection

from data import TILESETS, OBJECTS, ENEMIES, TEXTS, TILE_SIZE

fonts = ['drakoheart.ttf']

def init():
    ServerConnection.createDirectories()
    loadTileset()
    loadObjects()
    loadEnemies()
    loadFonts()

    main_directory = ServerConnection.getMainDirectory()
    pyglet.resource.path.append(main_directory + '/bgm')
    pyglet.resource.reindex()

    ServerConnection.getClientPath('img/gui/gui.png')
    ServerConnection.getClientPath('bgm/main_screen.ogg')


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