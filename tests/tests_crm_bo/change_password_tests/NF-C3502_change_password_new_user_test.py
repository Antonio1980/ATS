# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from test_definitions import BaseConfig
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from src.base.instruments import write_file_result, update_test_case


@test(groups=['change_password_page', ])
class ChangePasswordNewUserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3502'
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.email = cls.login_page.email
        cls.password = cls.login_page.password

    @test(groups=['sanity', 'functional', 'positive', ])
    def test_change_password_new_user(self):
        delay = 1
        result = False
        try:
            result = self.login_page.login(self.driver, self.login_page.email, self.login_page.password)
        finally:
            if result is True:
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
