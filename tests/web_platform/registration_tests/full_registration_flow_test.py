# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from tests.web_platform.pages.home_page import HomePage
from src.test_utils.testrail_utils import update_test_case
from tests.web_platform.pages.open_account_page import OpenAccountPage


@test(groups=['functional', 'smoke', 'sanity'])
class RegistrationFlowTest(unittest.TestCase, HomePage, OpenAccountPage):
    @classmethod
    def setUpClass(cls):
        cls.setup_open_account_page()
        cls.set_up_home_page()
        cls.get_browser(Browsers.CHROME.value)
        cls.test_case = '3521'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @classmethod
    @test(groups=['login_page', 'positive'])
    def test_registration_flow(cls):
        print(cls.open_account_url)
        delay = 1
        result1, result2 = False, False
        try:
            cls.go_to_home_page()
            result1 = cls.click_on_sign_up(delay)
            result2 = cls.registration_flow(delay)
        finally:
            if (result1 & result2) is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()











