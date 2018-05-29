# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.test_definitions import BaseConfig
from src.test_utils.testrail_utils import update_test_case
from tests.crm_bo.pages.login_page import LogInPage
from src.test_utils.file_utils import get_credentials_positive


@test(groups=['functional', 'smoke', 'sanity'])
class LogInTest(unittest.TestCase, LogInPage):
    @classmethod
    def setUpClass(cls):
        cls.get_browser("chrome")
        cls.test_case = '2590'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_login_positive(cls):
        delay = 1
        # 0, 0, 1 - row, column1, column2
        credentials = get_credentials_positive(BaseConfig.CRM_LOGIN_DATA, 0, 0, 1)
        username = credentials['username']
        password = credentials['password']
        result = None
        try:
            result = cls.login(delay, username, password)
        finally:
            if result is True:
                # server_url, test_case, status
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()











