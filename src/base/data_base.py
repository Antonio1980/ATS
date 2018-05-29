# !/usr/bin/env python
# -*- coding: utf8 -*-

import pymysql
from src.test_definitions import BaseConfig


class DataBase(object):
    @classmethod
    def setup_db(cls):
        cls.host = BaseConfig.DB_HOST
        cls.username = BaseConfig.DB_USERNAME
        cls.password = BaseConfig.DB_PASSWORD

    @classmethod
    def run_query(cls, db_name, query):
        cls.connection = pymysql.connect(host=cls.host, user=cls.username, passwd=cls.password, database=db_name)
        cls.cursor = cls.connection.cursor()
        cls.cursor.execute(query)
        rows = cls.cursor.fetchall()
        return rows

    @classmethod
    def close_db(cls):
        cls.connection.commit()
        cls.connection.close()

