# -*- coding: utf-8 -*-
import MySQLdb
import time
import datetime
import random
import os

from ud_exception import UDungeonException

DB_SERVER = 'udungeonA.gsmproductions.com'
DB_USER = '1gamuser_dev'
PASSWORD = '1gameamonth'
SCHEMA = 'udungeon'


class DBConnection:

    def __init__(self):
        pass

    def __getConnection(self):

        connect = MySQLdb.connect(DB_SERVER,DB_USER,PASSWORD,SCHEMA)
        return connect

    def __getCursor(self,sql,commit=False):


        db = self.__getConnection()

        try:   
            cursor  = db.cursor()
            cursor.execute(sql)
            
            if commit:
                db.commit()
        except:
            db.rollback()
        finally:
            db.close()

        return cursor

    def __convert(self, val):

        if type(val) == str:
            val = "'" + val + "'"
        else:
            val = str(val)

        return val

    def __insert(self,table,data):
        pass

    def __update(self, table, id, data):
        pass

    @staticmethod
    def getResult(sql):
        db = DBConnection()
        cursor = db.__getCursor(sql)

        data = cursor.fetchall()

        return data

    @staticmethod
    def getRoom(room_id):

        db = DBConnection()

        sql  = 'select roo_name, til_name '
        sql += 'from room '
        sql += 'inner join tileset on roo_til_xid = til_id '
        sql += 'where roo_id = ' + str(room_id)

        room =  {
                'name' :    None,
                'tileset' : None,
                'objects': {},
                'enemies': {}
                }

        cursor = db.__getCursor(sql)
        data = cursor.fetchone()

        if data != None:
            room['name'] = data[0]
            room['tileset'] = data[1]

        sql  = 'select obj_name, obj_type, rob_x, rob_y '
        sql += 'from room_object '
        sql += 'inner join object on rob_obj_xid = obj_id '
        sql += 'where rob_roo_xid = ' + str(room_id)

        cursor = db.__getCursor(sql)
        data = cursor.fetchall()

        for obj in data:
            pos = obj[2],obj[3]
            name = obj[0]
            typ = obj[1]

            room['objects'][pos] =  {
                                    'name' : name,
                                    'type' : typ
                                    }

        sql  = 'select ene_name, ren_x, ren_y, ren_ene_lvl '
        sql += 'from room_enemy '
        sql += 'inner join enemy on ren_ene_xid = ene_id '
        sql += 'where ren_roo_xid = ' + str(room_id)

        cursor = db.__getCursor(sql)
        data = cursor.fetchall()

        for ene in data:
            pos = ene[1],ene[2]
            enemy = ene[0],ene[3]

            room['enemies'][pos] = enemy

        return room

    @staticmethod
    def getUser(nickname):

        db = DBConnection()

        #--> code qui cache l'identitée du joueur
        _nickname = nickname
        
        if os.path.exists('user_id.dat'):
            f = open('user_id.dat','r')
            nickname = f.read()
            f.close()
        else:
            nickname = str(random.randint(0,99999))
            f = open('user_id.dat','w')
            f.write(nickname)
            f.close()

        #<--
        sql  = "select get_user('" + nickname + "')"

        cursor = db.__getCursor(sql,commit=True)
        data = cursor.fetchone()

        if data == None:
            raise UDungeonException("User " +  str(nickname) + " not found.")

        user =  {
                'name' : _nickname,
                'id' : data[0]
                }

        return user