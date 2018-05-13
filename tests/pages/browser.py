# !/usr/bin/env python
# -*- coding: utf8 -*-
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from tests_sources.drivers.webdriver_factory import WebDriverFactory


class Browser():
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
    def driver_wait(self, delay):
        return WebDriverWait(self.driver, delay)
        

    @classmethod
    def search_element(self, delay, locator):
        driver = self.driver
        try:
            element = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, locator)))
            return element
        except TimeoutException:
            print("Loading took to much time.")


    @classmethod
    def search_and_type(self, delay, query, locator):
        element = self.search_element(delay, locator)
        element.clear()
        element.send_keys(query)
        return element

    @classmethod
    def refresh_page(self):
        driver = self.driver
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')


    @classmethod
    def search_wait_click(self, delay, locator):
        #driver = self.driver
        try:
            self.search_element(delay, locator)
            return self.driver_wait_element_present(delay, locator).click()
        except TimeoutException:
            print("Loading took to much time.")
        #element.click()
        #return element


    @classmethod
    def driver_wait_element_present(self, delay, locator):
        driver = self.driver
        try:
            element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, locator)))
            return element
        except TimeoutException:
            print("Loading took to much time.")


    @classmethod
    def driver_wait_element_clickable(self, delay, locator):
        driver = self.driver
        try:
            element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, locator)))
            return element
        except TimeoutException:
            print("Loading took to much time.")


    @classmethod
    def tearDownClass(self):
        self.driver.delete_all_cookies()
        self.driver.quit()
