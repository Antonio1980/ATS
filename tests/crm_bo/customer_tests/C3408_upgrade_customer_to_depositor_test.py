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


class CustomerUpgradeStatusTest(unittest.TestCase, LogInPage, HomePage, CustomerPage):
    @classmethod
    def setUpClass(cls):
        cls.setup_login_page()
        cls.setup_home_page()
        cls.setup_customer_page()
        cls.get_browser(Browsers.CHROME.value)
        cls.test_case = '3408'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_customer_status_upgrade(cls):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = cls.login_positive(delay, cls.base_url)
            result2 = cls.choose_customer_by_name(delay)
            result3 = cls.make_deposit(delay)
        finally:
            if (result1 & result2 & result3) is True:
                if cls.check_customer_icon() == 'Depositor':
                    update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDown(cls):
        cls.close_browser()


