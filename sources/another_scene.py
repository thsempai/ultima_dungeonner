# -*- coding: utf-8 -*-
import cocos

from data import CREDITS
from translation import getTranslation

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

def gameoverScene():

    sc = cocos.scene.Scene()

    y = 300

    text = getTranslation('FAIL')
    label = cocos.text.Label(text,position = (400,y), font_name = 'Drakoheart Leiend', font_size = 40, anchor_x = 'center')
    sc.add(label)

    sc = cocos.scenes.transitions.ZoomTransition(sc)
    
    return sc  

def victoryScene():

    sc = cocos.scene.Scene()

    y = 300

    text = getTranslation('VICTORY')
    label = cocos.text.Label(text,position = (400,y), font_name = 'Drakoheart Leiend', font_size = 40, anchor_x = 'center')
    
    sc = cocos.scenes.transitions.ZoomTransition(sc)
    
    sc.add(label)

    return sc  
