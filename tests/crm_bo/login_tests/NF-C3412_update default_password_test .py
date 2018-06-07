# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from src.test_utils.testrail_utils import update_test_case
from tests.crm_bo.pages.customer_page import CustomerPage
from tests.crm_bo.pages.home_page import HomePage
from tests.crm_bo.pages.login_page import LogInPage


@test(groups=['login_page', 'positive'])
class UpdateDefaultPasswordTest(unittest.TestCase, LogInPage, HomePage, CustomerPage):
    @classmethod
    def setUpClass(cls):
        cls.get_browser(Browsers.CHROME.value)
        cls.test_case = '3412'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.setup_login_page()

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_update_default_password(cls):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = cls.login_positive(delay)

        finally:
            if (result1 & result2 & result3) is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDown(cls):
        cls.close_browser()