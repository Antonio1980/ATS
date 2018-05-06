# !/usr/bin/env python
# -*- coding: utf8 -*-
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from tests.tests_base.page_base import BasePage
from tests_extensions.tests_definitions import BaseConfig
from tests_resources.locators.home_page_locators import HomePageLocators
from tests_resources.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    @classmethod
    def login(self, username, password):
        self.go_to_page(BaseConfig.BASE_URL)
        self.driver_wait(3)
        #self.wait(1).until(EC.presence_of_element_located(By.XPATH, LogInPageLocators.CRM_LOGO))
        self.driver.find_element_by_xpath(LogInPageLocators.CRM_LOGO)
        self.search_type(LogInPageLocators.USERNAME_FIELD, username)
        self.search_type(LogInPageLocators.PASSWORD_FIELD, password)
        self.search_click(LogInPageLocators.LOGIN_BUTTON)
        self.driver_wait(2)
        self.driver.find_element_by_xpath(HomePageLocators.HOME_PAGE_LOGO)
        self.driver_wait(1)

    @classmethod
    def logout(self):
        self.driver_wait(1)
        self.driver.find_element_by_xpath(HomePageLocators.HOME_PAGE_LOGO)
        self.search_click(HomePageLocators.SETTINGS_DROPDOWN)
        self.search_click(HomePageLocators.LOGOFF_BUTTON)
        self.driver.find_element_by_xpath(LogInPageLocators.CRM_LOGO)
        self.driver_wait(1)



if __name__ == '__main__':
    pass



