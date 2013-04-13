# -*- coding: utf-8 -*-
import cocos
import pyglet
import getpass


from initialization import init
from db_connection import DBConnection
from server_connection import ServerConnection

from data import TILESETS, OBJECTS, ENEMIES, TEXTS, TILE_SIZE

from dungeon import Dungeon, Room
from db_connection import DBConnection
from server_connection import ServerConnection
from user import User
from menu import MainMenu, MENU_TRANSITION
from another_scene import creditsScene
from loader import LoaderScene
from ud_exception import UDungeonException
from translation import getTranslation

from data import SCREEN_SIZE, TITLE


class MainScene(cocos.scene.Scene):

    def __init__(self):

        cocos.scene.Scene.__init__(self)

        user = DBConnection.getUser(getpass.getuser())

        user = User(user)
        hero = user.getHero()

        dungeon = Dungeon(hero)
        cocos.director.director.window.push_handlers(dungeon)
        
        credits_scene = creditsScene()


        #main scene

        main_command =  [
                        (getTranslation('PLAY'),play,[dungeon.rooms[0]]),
                        (getTranslation('CREDITS'),play,[credits_scene]),
                        (getTranslation('QUIT'),cocos.director.director.window.close,[])
                        ]

        menu =  MainMenu(main_command)

        #Title
        label = cocos.text.Label(TITLE,position = (400,500), font_name = 'Drakoheart Leiend', font_size = 45, anchor_x = 'center')
        self.add(label)

        self.add(menu)

        #music
        bgm = ServerConnection.getMusic('bgm/main_screen.ogg')
        bgm_player = pyglet.media.Player()
        bgm_player.queue(bgm)
        bgm_player.eos_action = bgm_player.EOS_LOOP
        bgm_player.play()

def play(scene):
    
    scene = MENU_TRANSITION(scene)
    cocos.director.director.push(scene)

def main():

    #instancification de la fenêtre
    cocos.director.director.init(width=SCREEN_SIZE[0], height=SCREEN_SIZE[1], caption=TITLE)
    

    try:
        logo = ServerConnection.getImage('img/gui/logo.png')
        cocos.director.director.window.set_icon(logo)
    except:
        pass

    try:
        
        initial_scene = LoaderScene()
        initial_scene.set_loading(init(),MainScene)

        cocos.director.director.run(initial_scene)

    except UDungeonException as ude:
        print ude.message

if __name__ == "__main__":
    main()