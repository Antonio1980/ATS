# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import data, unpack, ddt
from src.base.enums import Browsers
from src.test_definitions import BaseConfig
from src.test_utils.file_utils import get_csv_data
from tests.web_platform.pages.home_page import HomePage
from src.test_utils.testrail_utils import update_test_case
from tests.web_platform.pages.open_account_page import OpenAccountPage


@test(groups=['functional', 'smoke', 'sanity'])
@ddt
class RegistrationTestDDT(unittest.TestCase, HomePage, OpenAccountPage):
    @classmethod
    def setUpClass(cls):
        cls.setup_open_account_page()
        cls.get_browser(Browsers.CHROME.value)
        cls.test_case = '3521'
        cls.test_run = BaseConfig.TESTRAIL_RUN

    @test(groups=['login_page', 'positive'])
    @data(*get_csv_data(BaseConfig.OPEN_ACCOUNT_DATA))
    @unpack
    def test_registration_ddt(cls, firstname, lastname, email, password):
        delay = 1
        result1, result2, result3 = False, False, False
        try:
            result1 = cls.go_to_home_page()
            result2 = cls.click_on_sign_up(delay)
            result3 = cls.registration_flow_ddt(firstname, lastname, email, password)
        finally:
            if (result1 & result2 & result3) is True:
                update_test_case(cls.test_run, cls.test_case, 1)
            else:
                update_test_case(cls.test_run, cls.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        cls.close_browser()











