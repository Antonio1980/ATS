# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.enums import Browsers
from tests.test_definitions import BaseConfig
from src.test_utils.file_utils import write_file_result
from src.test_utils.testrail_utils import update_test_case
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage


@test(groups=['open_account_page', 'e2e', ])
class RegistrationFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flag = False
        cls.test_case = '3750'
        cls.home_page = HomePage()
        cls.signup_page = SignUpPage()
        cls.email = cls.signup_page.email
        cls.phone = cls.signup_page.phone
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.password = cls.signup_page.password
        cls.first_last_name = cls.signup_page.first_last_name
        cls.driver = WebDriverFactory.get_browser(Browsers.CHROME.value)


    @test(groups=['regression', 'functional', 'positive', ], depends_on_groups=["smoke", "sanity", ])
    def test_registration_flow(self):
        delay = 1
        result1, result2, result3, result4 = False, False, False, False
        try:
            result1 = self.home_page.open_signup_page(self.driver, delay)
            result2 = self.signup_page.fill_signup_form(self.driver, self.first_last_name, self.email, self.password)
            # 1 - get_updates, 2 - click on change_password, 3 - click on verify_email
            new_password_url = self.signup_page.get_email_updates(self.driver, self.email, 0)
            token = new_password_url.split('=')
            token = token[1].split('&')[0]
            result3 = self.signup_page.get_email_updates(self.driver, self.email, 3, new_password_url)
            result4 = self.signup_page.add_phone(self.driver, self.phone)
        finally:
            if result1 and result2 and result3 and result4 is True:
                self.flag = True
                write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 1)
            else:
                write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", BaseConfig.WTP_TESTS_RESULT)
                update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        if cls.flag is True:
            write_file_result(cls.first_last_name + "," + cls.email + "," + cls.password + "\n",
                              BaseConfig.WTP_TESTS_CUSTOMERS)
        cls.home_page.close_browser(cls.driver)

