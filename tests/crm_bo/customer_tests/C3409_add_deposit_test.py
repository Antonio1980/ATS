# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from tests.crm_bo.pages.home_page import HomePage
from tests.crm_bo.pages.login_page import LogInPage
from tests.crm_bo.pages.customer_page import CustomerPage
from src.drivers.webdriver_factory import WebDriverFactory
from src.test_utils.testrail_utils import update_test_case


@test(groups=['end2end_tests', 'functional', 'sanity'])
class AddDepositTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.customer_page = CustomerPage()
        cls._driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3409'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_add_deposit(cls):
        delay = 1
        amount = 100
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = cls.login_page.login_positive(cls._driver, delay)
            result2 = cls.home_page.choose_customer_by_name(cls._driver, delay)
            result3 = cls.customer_page.make_deposit(cls._driver, delay, amount)
            result4 = cls.customer_page.check_balance(cls._driver, delay)
        finally:
            if (result1 & result2 is True) & (result3 & result4 is True):
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls._driver)
