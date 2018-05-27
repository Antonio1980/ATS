# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.enums import DriverHelper
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from src.drivers.webdriver_factory import WebDriverFactory
from selenium.webdriver.support import expected_conditions as EC


class Browser(object):
    @classmethod
    def get_browser(self, browser_name):
        """
        Set up method of class Browser.
        Calling WebDriverFactory to return needed driver instance.
        :param browser_name: string passed as parameter of browser type.
        :rtype: web driver object with implicite wait of 2 sec.
        """
        self.driver = WebDriverFactory.get_browser(browser_name)
        self.driver.maximize_window()
        return self.driver_wait(2)

    @classmethod
    def get_driver(self):
        """
        Provides ability to get driver from any place.
        :return: current web driver instance.
        """
        return self.driver

    @classmethod
    def go_to_url(self, url):
        """
        Browse the given url by existing driver instance.
        :param url: string url to open.
        :return: web driver object with implicite wait of 3 sec.
        """
        self.driver.get(url)
        return self.driver_wait(3)

    @classmethod
    def refresh_page(self):
        """
        Refresh browser page by sending 'Ctrl + r' keys.
        :return: web driver object with implicite wait of 3 sec.
        """
        self.driver_wait(1)
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')
        return self.driver_wait(3)

    @classmethod
    def refresh_browser(self):
        """
        Refresh browser by buildin optoin.
        :return: web driver
        """
        return self.driver.navigate().refresh()

    @classmethod
    def close_driver_instance(self):
        """
        Close web driver instance.
        """
        self.driver.delete_all_cookies()
        self.driver.close()

    @classmethod
    def driver_wait(self, delay):
        """
        Implicit wait for given delay.
        :param delay: seconds to wait.
        :return: web driver object.
        """
        return WebDriverWait(self.driver, delay)

    @classmethod
    def get_span_text(self, locator):
        """
        
        :param locator:
        :return:
        """
        element = self.find_element(locator)
        return element.get_attribute("innerHTML")

    @classmethod
    def get_text(self, locator):
        """

        :param locator:
        :return:
        """
        element = self.find_element(locator)
        return element.get_text()

    @classmethod
    def get_attribute_from_locator(self, locator, attribute):
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    @classmethod
    def get_attribute_from_element(self, element, attribute):
        """

        :param element:
        :param attribute:
        :return:
        """
        return element.get_attribute(attribute)

    @classmethod
    def send_keys(self, delay, locator, query):
        """

        :param delay:
        :param locator:
        :param query:
        """
        element = self.wait_element_clickable(delay, locator)
        element.clear()
        element.send_keys(query)

    @classmethod
    def send_enter_key(self, delay, locator):
        """

        :param delay:
        :param locator:
        """
        element = self.wait_element_clickable(delay, locator)
        element.send_keys(Keys.ENTER)

    @classmethod
    def search_element(self, delay, locator):
        """

        :param delay:
        :param locator:
        :return:
        """
        try:
            element = self.wait_element_visible(delay, locator)
            return element
        except TimeoutException:
            print("Element not visible.")

    @classmethod
    def insert_text_into_element(self, delay, query, locator):
        """

        :param delay:
        :param query:
        :param locator:
        :return:
        """
        element = self.wait_element_clickable(delay, locator)
        element.click()
        element.clear()
        element.send_keys(query)
        return element

    @classmethod
    def click_on_element(self, delay, locator):
        """

        :param delay:
        :param locator:
        :return:
        """
        element = self.wait_element_clickable(delay, locator)
        # self.hover_over_element(locator)
        return element.click()

    # works only with id
    # @classmethod
    # def hover_over_element(self, locator):
    #     ActionChains(self.driver).move_to_element(locator).perform()

    @classmethod
    def switch_frame(self, delay, locator):
        """

        :param delay:
        :param locator:
        """
        self.driver.switch_to().frame(self.wait_element_presented(delay, locator))

    @classmethod
    def wait_element_visible(self, delay, locator):
        """

        :param delay:
        :param locator:
        :return:
        """
        try:
            element = WebDriverWait(self.driver, delay).until(EC.visibility_of_element_located((By.XPATH, locator)))
            return element
        except TimeoutException as e:
            print('{}: TimeoutException element not visible: {}'.format(self.__class__, e))

    @classmethod
    def wait_element_presented(self, delay, locator):
        """

        :param delay:
        :param locator:
        :return:
        """
        try:
            element = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, locator)))
            return element
        except TimeoutException as e:
            print('{}: TimeoutException element not present: {}'.format(self.__class__, e))

    @classmethod
    def wait_element_clickable(self, delay, locator):
        """

        :param delay:
        :param locator:
        :return:
        """
        try:
            element = WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.XPATH, locator)))
            return element
        except TimeoutException as e:
            print('{}: TimeoutException element not clickable: {}'.format(self.__class__, e))

    @classmethod
    def find_element(self, locator):
        """

        :param locator:
        :return:
        """
        try:
            element = self.driver.find_element_by_xpath(locator)
            return element
        except TimeoutException as e:
            print('{}: TimeoutException element not found: {}'.format(self.__class__, e))

    @classmethod
    def find_element_by(self, locator, by):
        """

        :param locator:
        :param by:
        :return:
        """
        by = by.lower()
        try:
            if by == DriverHelper.ID.value:
                return self.driver.find_element(By.ID, locator)
            elif by == DriverHelper.NAME.value:
                return self.driver.find_element(By.NAME, locator)
            elif by == DriverHelper.CLASS_NAME.value:
                return self.driver.find_element(By.CLASS_NAME, locator)
            elif by == DriverHelper.TAG_NAME.value:
                return self.driver.find_element(By.TAG_NAME, locator)
            elif by == DriverHelper.LINK_TEXT.value:
                return self.driver.find_element(By.LINK_TEXT, locator)
            elif by == DriverHelper.XPATH.value:
                return self.driver.find_element(By.XPATH, locator)
            elif by == DriverHelper.CSS_SELECTOR.value:
                return self.driver.find_element(By.CSS_SELECTOR)
            elif by == DriverHelper.PARTIAL_LINK_TEXT.value:
                return self.driver.find_element(By.PARTIAL_LINK_TEXT, locator)
            else:
                return self.driver.find_element(By.XPATH, locator)
        except TimeoutException as e:
            print('{}: TimeoutException element not found: {}'.format(self.__class__, e))

    @classmethod
    def find_located_element(self, delay, locator):
        """

        :param delay:
        :param locator:
        :return:
        """
        try:
            element = WebDriverWait(self.driver, delay).until(self.find_element(locator))
            return element
        except TimeoutException as e:
            print('{}: TimeoutException waiting for search input field: {}'.format(self.__class__, e))
            return False

    @classmethod
    def search_element_until_param_fields_appears(self, delay, locator):
        """

        :param delay:
        :param locator:
        :return:
        """
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
            print('{}: TimeoutException waiting for search param field: {}'.format(self.__class__, e))
            return False

    # @classmethod
    # def if_page_loaded(self, delay, page_elements):
    #     WebDriverWait(self.get_driver(), delay).all_elements.get(0).get_locator_by()

    # need to change for elements
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
    def close_browser(self):
        """
        Calling self method to close driver instance
        """
        self.close_driver_instance()
