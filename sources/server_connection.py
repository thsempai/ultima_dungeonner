# -*- coding: utf-8 -*-

import pyglet
import urllib2
import os

SERVER = 'http://sempai.gsmproductions.com/'

DIR_LIST =  [
            '~/.udungeon',
            '~/.udungeon/img',
            '~/.udungeon/img/tileset',
            '~/.udungeon/img/menu',
            '~/.udungeon/img/gui',
            '~/.udungeon/fonts',
            ]

class ServerConnection:

    def __init__(self):
        self.__main_directory = os.path.expanduser(DIR_LIST[0]) + '/'

    def __downloadFile(self,path):
        if not os.path.exists(self.__main_directory + path):

            u = urllib2.urlopen(SERVER + path)
            try:
                f = open(self.__main_directory + path,'w')
                try:
                    
                    f.write(u.read())
                finally:
                    f.close()

            finally:
                u.close()

        return self.__main_directory + path

    @staticmethod
    def createDirectories():

        for path in DIR_LIST:
            #ajout le "/home" (ou autre si autre OS)
            path = os.path.expanduser(path)
            if not os.path.exists(path):
                os.makedirs(path)

    @staticmethod
    def getClientPath(path):

        sc = ServerConnection()
        return sc.__downloadFile(path)

    @staticmethod
    def getImage(path,region = None):
        if region == None:
            return pyglet.image.load(ServerConnection.getClientPath(path))
        else:
            return pyglet.image.load(ServerConnection.getClientPath(path)).get_region(*region)

