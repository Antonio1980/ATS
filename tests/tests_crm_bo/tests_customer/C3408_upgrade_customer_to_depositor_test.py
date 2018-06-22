# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.customer_page import CustomerPage


@test(groups=['customer_page', ])
class CustomerUpgradeStatusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.home_page = HomePage()
        cls.customer_page = CustomerPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3408'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['sanity', 'functional', 'positive', ])
    def test_customer_status_upgrade(cls):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = cls.login_page.login_positive(cls.driver, delay)
            result2 = cls.home_page.choose_customer_by_name(cls.driver, delay)
            result3 = cls.customer_page.make_deposit(cls.driver, delay)
        finally:
            if (result1 & result2 & result3) is True:
                if cls.customer_page.check_customer_icon(cls.driver) == 'Depositor':
                    update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDown(cls):
        cls.login_page.close_browser(cls.driver)
