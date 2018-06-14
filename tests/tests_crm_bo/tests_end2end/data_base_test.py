# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.data_base import DataBase
from tests.test_definitions import BaseConfig


@test(groups=['functional'])
class DataBaseTest(unittest.TestCase, DataBase):
    @classmethod
    def setUpClass(cls):
        cls.setup_db(BaseConfig.DB_HOST, BaseConfig.DB_USERNAME, BaseConfig.DB_PASSWORD)

    @classmethod
    @test(groups=['e2e'])
    def test_unit_db(cls):
        query = "Select * from " + BaseConfig.DB_TABLE + " ;"
        db_name = BaseConfig.DB_NAME
        print(cls.run_query(db_name, query))

    @classmethod
    def tearDown(cls):
        cls.close_db()


