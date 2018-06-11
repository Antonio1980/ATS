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
class CustomerUpgradeStatusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.customer_page = CustomerPage()
        cls._driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3408'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_customer_status_upgrade(cls):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = cls.login_page.login_positive(cls._driver, delay)
            result2 = cls.home_page.choose_customer_by_name(cls._driver, delay)
            result3 = cls.customer_page.make_deposit(cls._driver, delay)
        finally:
            if (result1 & result2 & result3) is True:
                if cls.customer_page.check_customer_icon(cls._driver) == 'Depositor':
                    update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDown(cls):
        cls.login_page.close_browser(cls._driver)
