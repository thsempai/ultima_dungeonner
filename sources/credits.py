# -*- coding: utf-8 -*-
import cocos

CREDITS =    [
            ('Game Design, code', ['Thomas Stassin']),
            ('Graphics' , ['Thomas Stassin']),
            ('Music' , ['Bastien Gorissen'])
            ]

def creditsScene():

    sc = cocos.scene.Scene()

    y = 500

    for text, names in CREDITS:
        label = cocos.text.Label(text,position = (400,y), font_name = 'Drakoheart Leiend', font_size = 40, anchor_x = 'center')
        sc.add(label)

        for name in names:
            y-=60
            label = cocos.text.Label(name,position = (400,y), font_name = 'Drakoheart Leiend', font_size = 30, anchor_x = 'center')
            sc.add(label)
        
        y-= 100

    return sc 
