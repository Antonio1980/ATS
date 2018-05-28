# !/usr/bin/env python
# -*- coding: utf8 -*-

import pymysql


class DataBase(object):
    def __init__(self, db):
        self.host = db['host']
        self.username = db['username']
        self.password = db['password']
        self.db_name = db['db_name']
        self.table = db['table']
        self.query = "Select * from " + self.table + " ;"

    @classmethod
    def run_query(cls):
        cls.connection = pymysql.connect(host=cls.host, user=cls.username, passwd=cls.password, database=cls.db_name)
        cls.cursor = cls.connection.cursor()
        cls.cursor.execute(cls.query)
        rows = cls.cursor.fetchall()
        cls.connection.commit()
        cls.connection.close()
        return rows

