# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from tests.crm_bo.pages.home_page import HomePage
from tests.crm_bo.pages.login_page import LogInPage
from tests.crm_bo.pages.customer_page import CustomerPage
from src.test_utils.testrail_utils import update_test_case


class AddDepositTest(unittest.TestCase, LogInPage, HomePage, CustomerPage):
    @classmethod
    def setUpClass(cls):
        cls.setup_login_page()
        cls.setup_home_page()
        cls.get_browser(Browsers.CHROME.value)
        cls.test_case = '3409'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_add_deposit(cls):
        delay = 1
        amount = 100
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = cls.login_positive(delay, cls.base_url)
            result2 = cls.choose_customer_by_name(delay)
            result3 = cls.make_deposit(delay, amount)
            result4 = cls.check_balance(delay)
        finally:
            if (result1 & result2 & result3 & result4) is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()