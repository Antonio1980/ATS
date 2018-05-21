# !/usr/bin/env python
# -*- coding: utf8 -*-

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.drivers.webdriver_factory import WebDriverFactory


class Browser(object):
    @classmethod
    def set_up_class(self, browser_name):
        self.driver = WebDriverFactory.get_browser(browser_name)
        self.driver.maximize_window()
        self.driver_wait(2)

    @classmethod
    def go_to_url(self, url):
        self.driver.get(url)
        return self.driver_wait(5)

    @classmethod
    def refresh_page(self):
        self.driver_wait(1)
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')
        return self.driver_wait(3)

    @classmethod
    def refresh_browser(self):
        return self.driver.navigate().refresh()

    @classmethod
    def close_driver_instance(self):
        self.driver.delete_all_cookies()
        self.driver.close()

    @classmethod
    def get_driver(self):
        return self.driver

    @classmethod
    def driver_wait(self, delay):
        return WebDriverWait(self.driver, delay)

    @classmethod
    def get_span_text(self, locator):
        element = self.find_element(locator)
        return element.get_attribute("innerHTML")

    @classmethod
    def get_text(self, locator):
        element = self.find_element(locator)
        return element.get_text()

    @classmethod
    def get_attribute_from_locator(self, locator, attribute):
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    @classmethod
    def get_attribute_from_element(self, element, attribute):
        return element.get_attribute(attribute)

    @classmethod
    def send_keys(self, delay, locator, query):
        element = self.wait_element_clickable(delay, locator)
        element.send_keys(query)

    @classmethod
    def send_enter_key(self, delay, locator):
        element = self.wait_element_clickable(delay, locator)
        element.send_keys(Keys.ENTER)

    @classmethod
    def search_element(self, delay, locator):
        try:
            element = self.wait_element_visible(delay, locator)
            return element
        except TimeoutException:
            print("Element not visible.")

    @classmethod
    def insert_text_into_element(self, delay, query, locator):
        element = self.wait_element_clickable(delay, locator)
        element.click()
        if element.get_attribute('value').length() > 0:
            element.clear()
        element.send_keys(query)
        return element

    # @classmethod
    # def if_page_loaded(self, delay, page_elements):
    #     WebDriverWait(self.get_driver(), delay).all_elements.get(0).get_locator_by()

    #need to change for elements
    # @classmethod
    # def print_objects_text(self, delay, locator):
    #     element = self.wait_element_presented(delay, locator)
    #     print(element.get_text())

    # need to change for elements
    # @classmethod
    # def get_num_of_elements(self, locator):
    #     elements = self.find_elements(locator)
    #     return elements.size()

    # @classmethod
    # def click_on_button(self, locator, index):
    #     self.find_elements(locator).get(index).click()

    # for purpose need to create check_checkbox method
    # @classmethod
    # def if_parent_element_exists(self, delay, locator, element):
    #     self.driver_wait(delay)
    #     result = element.find_elements(locator).size() != 0
    #     return result

    @classmethod
    def click_on_element(self, delay, locator):
        element = self.wait_element_clickable(delay, locator)
        self.hover_over_element(locator)
        return element.click()

    @classmethod
    def hover_over_element(self, locator):
        ActionChains(self.driver).move_to_element(locator).perform()

    @classmethod
    def switch_frame(self, delay, locator):
        self.driver.switch_to().frame(self.wait_element_presented(delay, locator))

    @classmethod
    def wait_element_visible(self, delay, locator):
        try:
            element = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, locator)))
            return element
        except TimeoutException as e:
            print('{}: TimeoutException element not visible: {}'.format(self.name, e))

    @classmethod
    def wait_element_presented(self, delay, locator):
        try:
            element = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, locator)))
            return element
        except TimeoutException as e:
            print('{}: TimeoutException element not present: {}'.format(self.name, e))

    @classmethod
    def wait_element_clickable(self, delay, locator):
        try:
            element = WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.XPATH, locator)))
            return element
        except TimeoutException as e:
            print('{}: TimeoutException element not clickable: {}'.format(self.name, e))

    @classmethod
    def find_element(self, locator):
        try:
            element = self.driver.find_element_by_xpath(locator)
            return element
        except TimeoutException as e:
            print('{}: TimeoutException element not found: {}'.format(self.name, e))

    @classmethod
    def find_located_element(self, delay, element):
        try:
            search_input = WebDriverWait(self.driver, delay).until(self.find_element(element))
            return search_input
        except TimeoutException as e:
            print('{}: TimeoutException waiting for search input field: {}'.format(self.name, e))
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
            print('{}: TimeoutException waiting for search param field: {}'.format(self.name, e))
            return False

    @classmethod
    def tear_down_class(self):
        self.close_driver_instance()
