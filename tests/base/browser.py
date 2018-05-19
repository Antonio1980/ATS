# !/usr/bin/env python
# -*- coding: utf8 -*-


from venv import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests_sources.drivers.webdriver_factory import WebDriverFactory


class Browser(object):
    @classmethod
    def setUpClass(self, browser_name):
        self.driver = WebDriverFactory.get_browser(browser_name)
        self.driver.maximize_window()
        self.driver_wait(2)


    @classmethod
    def go_to_page(self, url):
        self.driver.get(url)
        self.driver_wait(5)
        return self

    @classmethod
    def refresh_page(self):
        driver = self.driver
        self.driver_wait(1)
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')
        self.driver_wait(3)


    @classmethod
    def driver_wait(self, delay):
        return WebDriverWait(self.driver, delay)
        

    @classmethod
    def search_element(self, delay, locator):
        try:
            element = self.driver_wait_element_visible(delay, locator)
            return element
        except TimeoutException:
            print("Element not found.")


    @classmethod
    def search_and_type(self, delay, query, locator):
        element = self.driver_wait_element_clickable(delay, locator)
        element.clear()
        element.send_keys(query)
        return element


    @classmethod
    def search_and_click(self, delay, locator):
        element = self.driver_wait_element_clickable(delay, locator)
        self.driver_wait(delay)
        element.click()
        return element


    @classmethod
    def driver_wait_element_visible(self, delay, locator):
        try:
            element = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, locator)))
            return element
        except TimeoutException:
            print("Loading took to much time.")


    @classmethod
    def driver_wait_element_presented(self, delay, locator):
        try:
            element = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, locator)))
            return element
        except TimeoutException:
            print("Loading took to much time.")


    @classmethod
    def driver_wait_element_clickable(self, delay, locator):
        try:
            element = WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.XPATH, locator)))
            return element
        except TimeoutException:
            print("Loading took to much time.")


    @classmethod
    def find_element(self, locator):
        try:
            element = self.driver.find_element_by_xpath(locator)
            return element
        except TimeoutException:
            print("Element not found.")


    @classmethod
    def find_located_element(self, delay, element):
        try:
            search_input = WebDriverWait(self.driver, delay).until(self.find_element(element))
            return search_input
        except TimeoutException as e:
            logger.error('{}: TimeoutException waiting for search input field: {}'.format(self.name, e))
            return False


    @classmethod
    def search_element_until_param_fields_appears(self, delay, locator):

        def find_visible_search_param():
            for _, item in self.find_element(locator).items():
                fields = self.find_element(*item)
                if not fields:
                    return False
            return True

        try:
            element = WebDriverWait(self.webdriver, delay).until(find_visible_search_param)
            return element
        except TimeoutException as e:
            logger.error('{}: TimeoutException waiting for search param field: {}'.format(self.name, e))
            return False



    @classmethod
    def tearDownClass(self):
        self.driver.delete_all_cookies()
        self.driver.quit()