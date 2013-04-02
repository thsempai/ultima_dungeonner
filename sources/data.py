# -*- coding: utf-8 -*-
import cocos
import cocos.scenes

# donnée générale
SCREEN_SIZE = 800,600
TITLE = "Ultima Dungeonner alpha v0.01.1"

CREDITS =   [
            ('Game Design, code', ['Thomas Stassin']),
            ('Graphics' , ['Thomas Stassin']),
            ('Music' , ['Bastien Gorissen'])
            ]

#transition

MENU_TRANSITION = cocos.scenes.transitions.ZoomTransition

#server

SERVER = 'http://sempai.gsmproductions.com/'
DB_SERVER = 'udungeonA.gsmproductions.com'
DB_USER = '1gamuser_dev'
PASSWORD = '1gameamonth'
SCHEMA = 'udungeond'

#Dungeon
TILESETS    = {}
OBJECTS     = {}
ENEMIES     = {}

TEXTS       =   {
                    'enemy'     : {},
                    'object'    : {}
                }

TILE_SIZE = 32,32

TRAP_PROPERTY = {
                'hole' :            {
                                    'passable': False
                                    },
                'poisoned trap' :   {
                                    'passable' : True,
                                    'damage': 3
                                    }
                }

ITEM_PROPERTY = {
                'heal potion' : {
                                'healing' : 5
                                }
                }

#hero
N_ITEM = 3

#data
DIR_LIST =  [
            '~/.udungeon',
            '~/.udungeon/img',
            '~/.udungeon/img/tileset',
            '~/.udungeon/img/menu',
            '~/.udungeon/img/gui',
            '~/.udungeon/fonts',
            '~/.udungeon/bgm'
            ]