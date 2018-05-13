# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from ddt import ddt, data, unpack
from proboscis import test
from tests_sources.test_utils.file_util import get_csv_data
from tests.locators.home_page_locators import HomePageLocators
from tests.locators.login_page_locators import LogInPageLocators
from tests_sources.test_definitions import BaseConfig
from tests_sources.drivers.webdriver_factory import WebDriverFactory


@test(groups=['functional', 'smoke', 'sanity'])
@ddt
class LogInDDTTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.browser_name = "chrome"
        self.driver = WebDriverFactory.get_browser(self.browser_name)
        self.driver.implicitly_wait(1)
        self.driver.maximize_window()

    @test(groups=['login_page', 'ddt'])
    @data(*get_csv_data(BaseConfig.W_TEST_DATA))
    @unpack
    def test_login(self, username, password):
        driver = self.driver
        driver.get(BaseConfig.CRM_BASE_URL)
        user_field = driver.find_element_by_xpath(LogInPageLocators.USERNAME_FIELD)
        user_field.clear()
        user_field.send_keys(username)
        password_field = driver.find_element_by_xpath(LogInPageLocators.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)
        login_button = driver.find_element_by_xpath(LogInPageLocators.LOGIN_BUTTON)
        login_button.click()
        assert driver.find_element_by_xpath(HomePageLocators.HOME_PAGE_LOGO)


    @classmethod
    def tearDownClass(slc):
        slc.driver.delete_all_cookies()
        slc.driver.quit()










