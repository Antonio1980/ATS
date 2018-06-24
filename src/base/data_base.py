# !/usr/bin/env python
# -*- coding: utf8 -*-

import pymysql
from tests.test_definitions import BaseConfig


class DataBase(object):
    def __init__(self):
        _host = BaseConfig.DB_HOST
        _username = BaseConfig.DB_USERNAME
        _password = BaseConfig.DB_PASSWORD
        _db_name = BaseConfig.DB_NAME
        _port = 30002
        self.connection = pymysql.connect(host=_host, port=_port, user=_username, passwd=_password, database=_db_name)

    def run_query(self, query):
        rows = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
        finally:
            self.connection.commit()
            self.connection.close()
            return rows
