# !/usr/bin/env python
# -*- coding: utf8 -*-

import pymysql


class DataBase(object):
    @classmethod
    def db_connect(cls):
        cls.connection = pymysql.connect(host="localhost", user="root", passwd="", database="databaseName")
        cls.cursor = cls.connection.cursor()

    @classmethod
    def create_table(cls):
        ArtistTableSql = """CREATE TABLE Artists(
        ID INT(20) PRIMARY KEY AUTO_INCREMENT,
        NAME  CHAR(20) NOT NULL,
        TRACK CHAR(10))"""
        cls.cursor.execute(ArtistTableSql)

    @classmethod
    def insert_into(cls):
        # queries for inserting values
        insert1 = "INSERT INTO Artists(NAME, TRACK) VALUES('Towang', 'Jazz' );"
        insert2 = "INSERT INTO Artists(NAME, TRACK) VALUES('Sadduz', 'Rock' );"
        # executing the quires
        cls.cursor.execute(insert1)
        cls.cursor.execute(insert2)

    @classmethod
    def select_all(cls):
        # queries for retrievint all rows
        retrive = "Select * from Artists;"
        # executing the quires
        cls.cursor.execute(retrive)
        rows = cls.cursor.fetchall()
        for row in rows:
            print(row)

    @classmethod
    def close_c0nnection(cls):
        cls.connection.commit()
        cls.connection.close()

