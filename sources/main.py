# -*- coding: utf-8 -*-
import cocos
import pyglet
import getpass


from initialization import InitLayer, SCREEN_SIZE, TITLE, UDungeonException



def test():

    #instancification de la fenêtre
    game = cocos.director.director.init(width=SCREEN_SIZE[0], height=SCREEN_SIZE[1], caption=TITLE)
    

    try:
        logo = ServerConnection.getImage('img/gui/logo.png')
        game.set_icon(logo)
    except:
        pass



    try:
        
        initial = InitLayer(game)
        cocos.director.director.run(initial)


    except UDungeonException as ude:
        print ude.message

if __name__ == "__main__":
    test()