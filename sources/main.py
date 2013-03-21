# -*- coding: utf-8 -*-
import cocos
import getpass

from dungeon import Dungeon, RoomScene
from initialization import init
from db_connection import DBConnection
from user import User
from ud_exception import UDungeonException

SCREEN_SIZE = 800,600

def test():
    title = "Ultima Dungeonner alpha v0.01"
    game = cocos.director.director.init(width=SCREEN_SIZE[0], height=SCREEN_SIZE[1], caption=title)
    
    try:
        user = DBConnection.getUser(getpass.getuser())

        user = User(user)
        hero = user.getHero()

        dungeon = Dungeon(hero)

        game.push_handlers(dungeon)
        
        cocos.director.director.run(dungeon[0])
    except UDungeonException as ude:
        print ude.message

if __name__ == "__main__":
    init()
    test()