# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.test_utils.testrail_utils import update_test_case
from tests.drivers.webdriver_factory import WebDriverFactory


@test(groups=['change_password_page', ])
class ChangePasswordPageUiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.login_page = LogInPage()
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3502'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['sanity', 'gui', 'positive', ])
    def test_change_password_page(cls):
        delay = 1
        result = False
        try:
            result = cls.login_page.login_positive(cls.driver, delay, cls.base_url)
        finally:
            if result is True:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "1 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                write_file_result(cls.test_case + "," + cls.test_run + "," + "0 \n", BaseConfig.CRM_TESTS_RESULT)
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.login_page.close_browser(cls.driver)
