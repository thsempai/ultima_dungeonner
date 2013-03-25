# -*- coding: utf-8 -*-
import cocos
import getpass

from dungeon import Dungeon, RoomScene
from initialization import init
from db_connection import DBConnection
from user import User
from menu import MainMenu, MENU_TRANSITION
from credits import creditsScene
from ud_exception import UDungeonException

SCREEN_SIZE = 800,600
TITLE = "Ultima Dungeonner alpha v0.01"

def play(scene):
    
    scene = MENU_TRANSITION(scene)
    cocos.director.director.push(scene)

def test():

    game = cocos.director.director.init(width=SCREEN_SIZE[0], height=SCREEN_SIZE[1], caption=TITLE)
    
    try:
        user = DBConnection.getUser(getpass.getuser())

        user = User(user)
        hero = user.getHero()

        dungeon = Dungeon(hero)
        game.push_handlers(dungeon)
        
        credits_scene = creditsScene()


        #main scene

        main_command =  [
                        ('Play',play,[dungeon[0]]),
                        ('Credits',play,[credits_scene]),
                        ('Quit',game.close,[])
                        ]

        main_scene =  cocos.scene.Scene()
        menu =  MainMenu(main_command)

        #Title
        label = cocos.text.Label(TITLE,position = (400,500), font_name = 'Drakoheart Leiend', font_size = 45, anchor_x = 'center')
        main_scene.add(label)

        main_scene.add(menu)

        cocos.director.director.run(main_scene)

    except UDungeonException as ude:
        print ude.message

if __name__ == "__main__":
    init()
    test()