# -*- coding: utf-8 -*-

import pyglet

class ControlerManager:

    def __init__(self):

        self.__types =  {
                        'dungeon':  {}
                        }

        self.__types['dungeon'] =   {
                                    'hero_left' :       None,
                                    'hero_right':       None,
                                    'hero_up'   :       None,
                                    'hero_down' :       None,
                                    'grid_visibility' : None,
                                    'call_menu' :       None
                                    }

        self.__keys = {}

        self.pause = False

    def __checkCommand(self,typ,command):
        try:
            if not self.__types.has_key(typ):
                raise Exception("Type '" + str(typ) +"'' don't exist.")

            if not self.__types[typ].has_key(command):
                raise Exception("Command '" + str(command) +" don't exist for type '"  + str(typ) + "'.")

        except Exception, e:
            raise e

    def defineCommand(self,typ,command,fonction,args=[],kwargs={}):
        
        self.__checkCommand(typ,command)
        self.__types[typ][command] = [fonction,args,kwargs]

    def mapCommand(self,typ,command,symbol):
        
        self.__checkCommand(typ,command)

        if not self.__keys.has_key(typ):
            self.__keys[typ] = {}

        self.__keys[typ][symbol] = command


    def onKeyRelease(self,typ,symbol,modifiers):
        
        if self.pause:
            return

        if self.__keys.has_key(typ):
            if self.__keys[typ].has_key(symbol):
                command = self.__keys[typ][symbol]

                fct, args, kwargs = self.__types[typ][command]
                fct(*args,**kwargs)

#singleton
CONTROLER = ControlerManager()

#mapping

CONTROLER.mapCommand('dungeon','hero_up',pyglet.window.key.Z)
CONTROLER.mapCommand('dungeon','hero_down',pyglet.window.key.S)
CONTROLER.mapCommand('dungeon','hero_left',pyglet.window.key.Q)
CONTROLER.mapCommand('dungeon','hero_right',pyglet.window.key.D)
CONTROLER.mapCommand('dungeon','grid_visibility',pyglet.window.key.G)
CONTROLER.mapCommand('dungeon','call_menu',pyglet.window.key.F12)
