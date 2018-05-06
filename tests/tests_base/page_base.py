# !/usr/bin/env python
# -*- coding: utf8 -*-
from telnetlib import EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from tests_extensions.webdriver_factory import WebDriverFactory


class BasePage:
    @classmethod
    def setUpClass(cls, browser_name):
        cls.driver = WebDriverFactory.get_browser(browser_name)
        cls.driver.maximize_window()

    @classmethod
    def go_to_page(self, url):
        self.driver.get(url)
        self.driver_wait(5)
        return self

    @classmethod
    def search_type(self, locator, query):
        self.element = self.driver_wait_until_clickable(locator)
        self.element.clear()
        self.driver_wait(1)
        self.element.send_keys(str(query))
        self.driver_wait(2)
        return self

    @classmethod
    def search_click(self, locator):
        #element = self.driver.find_element_by_xpath(locator)
        wait = self.driver_wait_until_clickable(locator)
        wait.click()
        self.driver_wait(2)
        return self

    @classmethod
    def driver_wait(self, args):
        WebDriverWait(self, args)

    @classmethod
    def driver_wait_until_present(self, locator):
        try:
            wait = self.driver_wait(10)
            return wait.until(EC.presence_of_element_located(By.XPATH, locator))
            #return WebDriverWait(self, 10).until(EC.presence_of_element_located(By.XPATH, locator))
        finally:
            assert self.driver.find_element_by_xpath(locator)


    @classmethod
    def driver_wait_until_clickable(self, locator):
        try:
            return self.driver_wait(10).until(EC.element_to_be_clickable((By.XPATH, locator)))
        finally:
            assert self.driver.find_element_by_xpath(locator)

    @classmethod
    def tearDownClass(slc):
        slc.driver.delete_all_cookies()
        slc.driver.quit()
