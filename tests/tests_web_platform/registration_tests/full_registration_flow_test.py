# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from tests.tests_web_platform.pages.home_page import HomePage
from src.test_utils.testrail_utils import update_test_case
<<<<<<< a6ac884835aaa047de5b5f6bf0e391f6806c43ed:tests/web_platform/registration_tests/full_registration_flow_test.py
from src.drivers.webdriver_factory import WebDriverFactory
from tests.web_platform.pages.open_account_page import OpenAccountPage
=======
from tests.tests_web_platform.pages.open_account_page import OpenAccountPage
>>>>>>> 46d3ea0049230292881d76fb45bbfa6fde5f95e8:tests/tests_web_platform/registration_tests/full_registration_flow_test.py


@test(groups=['functional', 'smoke', 'sanity'])
class RegistrationFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.open_account_page = OpenAccountPage()
        cls.home_page = HomePage()
        cls._driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
        cls.test_case = '3521'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_registration_flow(cls):
        delay = 1
        result1, result2 = False, False
        try:
            result1 = cls.home_page.open_signup_page(cls._driver, delay)
            result2 = cls.open_account_page.registration_flow(cls._driver, delay)
        finally:
            if (result1 & result2) is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.home_page.close_browser(cls._driver)
