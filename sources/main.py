# -*- coding: utf-8 -*-
import cocos

from dungeon import Dungeon, RoomScene
from character import Hero
from initialization import init

SCREEN_SIZE = 800,600

def test():
    title = "Ultimata Dungeonner alpha v0.01"
    game = cocos.director.director.init(width=SCREEN_SIZE[0], height=SCREEN_SIZE[1], caption=title)
    hero = Hero()
    dungeon = Dungeon(hero)

    game.push_handlers(dungeon)
    cocos.director.director.run(dungeon[0])

if __name__ == "__main__":
    init()
    test()