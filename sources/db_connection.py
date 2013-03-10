# -*- coding: utf-8 -*-
import MySQLdb

DB_SERVER = '1gamdb.gsmproductions.com'
DB_USER = '1gamuser_dev'
PASSWORD = '1gameamonth'
SCHEMA = '1gam201302'


class DBConnection:

    def __init__(self):
        pass

    def __getConnection(self):
        connect = MySQLdb.connect(DB_SERVER,DB_USER,PASSWORD,SCHEMA)
        return connect

    def __getCursor(self,sql):


        db = self.__getConnection()

        try:   
            cursor  = db.cursor()
            cursor.execute(sql)
        finally:
            db.close()

        return cursor

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

        sql  = 'select obj_name, rob_x, rob_y '
        sql += 'from room_object '
        sql += 'inner join object on rob_obj_xid = obj_id '
        sql += 'where rob_roo_xid = ' + str(room_id)

        cursor = db.__getCursor(sql)
        data = cursor.fetchall()

        for obj in data:
            pos = obj[1],obj[2]
            name = obj[0]

            room['objects'][pos] = name

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

