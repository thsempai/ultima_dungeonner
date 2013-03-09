# -*- coding: utf-8 -*-
import cocos

from dungeon import Dungeon, RoomScene
from character import Hero
from initialization import init

SCREEN_SIZE = 800,600

def test():

    cocos.director.director.init(width=SCREEN_SIZE[0], height=SCREEN_SIZE[1], caption="Ultimate Dungeonner")
    hero = Hero()
    dungeon = Dungeon(hero)

    cocos.director.director.run(dungeon[0])

if __name__ == "__main__":
    init()
    test()