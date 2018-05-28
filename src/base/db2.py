# !/usr/bin/env python
# -*- coding: utf8 -*-

# import mysql.connector
# from mysql.connector import errorcode
# from mysql.connector.cursor import MySQLCursor
#
# class DataBase(object):
#     def __init__(self, **kwargs):
#         self.connection_options = {}
#         self.connection_options['user'] = 'root'
#         self.connection_options['password'] = ''
#         self.connection_options['host'] = '192.168.33.10'
#         self.connection_options['port'] = '3306'
#         self.connection_options['database'] = "test"
#         self.connection_options['raise_on_warnings'] = True
#         self.connect()
#
#     def connect(self):
#         try:
#             self.cnx = mysql.connector.connect(**self.connection_options)
#         except mysql.connector.Error as err:
#             if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#                 print "Something is wrong with your user name or password"
#             elif err.errno == errorcode.ER_BAD_DB_ERROR:
#                 print "Database does not exists"
#             else:
#                 print err
#
#     def query(self, statement, data=''):
#         cursor = MySQLCursor(self.cnx)
#         cursor.execute(statement)
#         result = cursor.fetchall()
#         cursor.close
#         return result
#
#     def get_version(self):
#         print
#         self.query("select version()")
#
#     def chktable(self, tb_name):
#         tab = table(name=tb_name)
#         tab.check_table()
#
#
# class table(mysql_connection):
#     def __init__(self, **kwargs):
#         self.name = kwargs['name']
#
#     def check_table(self):
#         return super(table, self).query("show tables like '{}".format(self.name))
#
# conn = mysql_connection()
# conn.get_version()
# conn.chktable("test")
