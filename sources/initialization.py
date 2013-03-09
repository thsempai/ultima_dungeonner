
import cocos

from db_connection import DBConnection
from server_connection import ServerConnection
from dungeon import TILESETS, OBJECTS, TILE_SIZE

def init():
    ServerConnection.createDirectories()
    loadTileset()
    loadObjects()

def getTile(img,pos):
    return img.get_region(pos[0]*TILE_SIZE[0],pos[1]*TILE_SIZE[1],TILE_SIZE[0],TILE_SIZE[1])


def loadTileset():

    dic = {}

    sql =  "select til_name, til_path, tty_name "
    sql += "from tileset "
    sql += "inner join tileset_type on til_tty_xid = tty_id "

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
                prop =  {   'passable': True
                        }

                if n[:4] == 'wall':
                    prop['passable'] = False

                tileset.add( prop, getTile(img,p), n)
                dic[name] = tileset
        else:
            ServerConnection.getClientPath(path)

    global TILESETS
    TILESETS.update(dic)

def loadObjects():

    sql =  "select obj_name, til_path, obj_til_x, obj_til_y "
    sql += "from object "
    sql += "inner join tileset on obj_til_xid = til_id ";

    rows = DBConnection.getResult(sql)

    dic = {}

    for obj in rows:
        name = obj[0]
        region = obj[2], obj[3], TILE_SIZE[0], TILE_SIZE[1]
        path = obj[1]

        img = ServerConnection.getImage(path,region)

        dic['name'] = img

    global OBJECTS
    OBJECTS.update(dic)