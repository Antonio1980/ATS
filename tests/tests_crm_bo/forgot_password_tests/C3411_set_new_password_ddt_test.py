# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from ddt import data, unpack, ddt
from src.base.enums import Browsers
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages import reset_password_url
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory


@ddt
@test(groups=['login_page'])
class NewPasswordFlowDDTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_case = '3411'
        cls.login_page = LogInPage()
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.results_file = BaseConfig.CRM_TESTS_RESULT
        cls.forgotten_email = cls.login_page.forgotten_email
        cls.forgotten_username = cls.login_page.forgotten_username
        cls.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)

    @test(groups=['sanity', 'ddt', 'negative', ], depends_on_groups=["smoke", ])
    @data(*Instruments.get_csv_data(BaseConfig.CRM_NEW_PASSWORD_DATA))
    @unpack
    def test_new_password_flow_ddt(self, wrong_password):
        step1, step2, step3, step4 = False, False, False, True
        try:
            step1 = self.login_page.forgot_password(self.driver, self.forgotten_email, )
            # 0 - get_token for forgot password, 1 - get_token (new password) for regenerate password,
            # 2 - click on forgot_password, 3 - ?
            content = self.login_page.get_email_updates(self.driver, self.forgotten_email, 0)
            token = content.split('/')[-1]
            new_password_url = reset_password_url + token
            step2 = self.login_page.get_email_updates(self.driver, self.forgotten_email, 2, new_password_url)
            new_password = self.login_page.get_email_updates(self.driver, self.forgotten_email, 1)
            step3 = self.login_page.login(self.driver, self.forgotten_username, new_password)
            step4 = self.login_page.set_new_password(self.driver, new_password, wrong_password)
        finally:
            if step1 and step2 and step3 is True and step4 is False:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_result(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    @classmethod
    def tearDownClass(cls):
        Browser.close_browser(cls.driver)
