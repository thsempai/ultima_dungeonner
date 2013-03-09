# -*- coding: utf-8 -*-
from server_connection import ServerConnection

class Hero:

    def __init__(self):

        self.image = ServerConnection.getImage('img/tileset/hero.png')
