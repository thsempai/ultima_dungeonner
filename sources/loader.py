# -*- coding: utf-8 -*-

import cocos
from server_connection import ServerConnection

class LoaderScene(cocos.scene.Scene):

    def __init__(self):
        cocos.scene.Scene.__init__(self)

        text = 'Loading ... 0%'

        self.label = cocos.text.Label(text,position = (400,300), font_name = 'Drakoheart Leiend', font_size = 40, anchor_x = 'center')
        self.add(self.label)
        self.schedule(self.__callback)

        self.generator = None
        self.next = None
        self.done = False

    def set_loading(self,generator,next):

        self.next = next
        self.generator = generator

    def __callback(self,dt):
        
        if self.generator != None:  
            try:
                result = self.generator.next()
                self.label.element.text = 'Loading ... ' + str(int(result*100)) + '%'
            except StopIteration as e:
                cocos.director.director.replace(self.next())