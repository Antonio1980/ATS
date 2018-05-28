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
    # def __init__(self, *browser_name):
    #     if browser_name:
    #         self.driver = WebDriverFactory.get_browser(browser_name)
    #     else:
    #         self.driver = WebDriverFactory.get_browser("chrome")

    @classmethod
    def get_browser(cls, browser_name):
        """
        Set up method of class Browser.
        Calling WebDriverFactory to return needed driver instance.
        :param browser_name: string passed as parameter of browser type.
        :return: web driver object with implicite wait of 2 sec.
        """
        cls.driver = WebDriverFactory.get_browser(browser_name)
        cls.driver.maximize_window()
        return cls.driver_wait(2)

    @classmethod
    def get_driver(cls):
        """
        Provides ability to get driver from any place.
        :return: current web driver instance.
        """
        return cls.driver

    @classmethod
    def go_to_url(cls, url):
        """
        Browse the given url by existing driver instance.
        :param url: string url to open.
        :return: web driver object with implicite wait of 3 sec.
        """
        cls.driver.get(url)
        return cls.driver_wait(3)

    @classmethod
    def refresh_page(cls):
        """
        Refresh browser page by sending 'Ctrl + r' keys.
        :return: web driver object with implicite wait of 3 sec.
        """
        cls.driver_wait(1)
        cls.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')
        return cls.driver_wait(3)

    @classmethod
    def refresh_browser(cls):
        """
        Refresh browser by navigating on 'refresh' button.
        :return: web driver.
        """
        return cls.driver.navigate().refresh()

    @classmethod
    def close_driver_instance(cls):
        """
        Close web driver instance.
        """
        cls.driver.delete_all_cookies()
        cls.driver.close()

    @classmethod
    def driver_wait(cls, delay):
        """
        Implicit wait for given delay.
        :param delay: seconds to wait.
        :return: web driver object.
        """
        return WebDriverWait(cls.driver, delay)

    @classmethod
    def get_span_text(cls, locator):
        """
        Get attribute text of a web element.
        :param locator: xpath string.
        :return: span tag of a web element.
        """
        try:
            element = cls.find_element(locator)
            return element.get_attribute("innerHTML")
        except TimeoutException:
            print("Element not found.")

    @classmethod
    def get_text(cls, locator):
        """
        Get text of a web element.
        :param locator: xpath string.
        :return: text of a web element if exists.
        """
        try:
            element = cls.find_element(locator)
            return element.get_text()
        except TimeoutException:
            print("Element not found.")

    @classmethod
    def get_attribute_from_locator(cls, locator, attribute):
        """
        Get an attribut from a web element.
        :param locator: xpath string.
        :param attribute: needed attribute.
        :return: web element attribute.
        """
        try:
            element = cls.find_element(locator)
            return element.get_attribute(attribute)
        except TimeoutException:
            print("Element not found.")

    @classmethod
    def get_attribute_from_element(cls, element, attribute):
        """
        Get an attribute from a web element.
        :param element: web element.
        :param attribute: needed attribute.
        :return: attribute of a web element.
        """
        try:
            return element.get_attribute(attribute)
        except TimeoutException:
            print("Element not exists.")

    @classmethod
    def send_keys(cls, element, query):
        """
        Type a text into web element directly.
        :param element: web element.
        :param query: text to type.
        :return: driver state.
        """
        try:
            element.clear()
            return element.send_keys(query)
        except TimeoutException:
            print("Element not clickable.")

    @classmethod
    def send_enter_key(cls, element):
        """
        Push the enter key on web element.
        :param element: web element.
        :return: driver state.
        """
        try:
            return element.send_keys(Keys.ENTER)
        except TimeoutException:
            print("Element not clickable.")

    @classmethod
    def search_element(cls, delay, locator):
        """
        Search a web element.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            if cls.wait_element_presented(delay, locator):
                return cls.wait_element_clickable(delay, locator)
        except TimeoutException:
            print("Element not visible.")

    @classmethod
    def type_text_by_locator(cls, delay, locator, query):
        """
        Clear and type text into web element.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :param query: text to type.
        :return: driver state.
        """
        try:
            element = cls.search_element(delay, locator)
            element.click()
            element.clear()
            return element.send_keys(query)
        except TimeoutException:
            print("Element not clickable.")

    @classmethod
    def click_on_element_by_locator(cls, delay, locator):
        """
        Search and click on a web element.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: driver state.
        """
        try:
            element = cls.wait_element_clickable(delay, locator)
            # cls.hover_over_element(locator)
            return element.click()
        except TimeoutException:
            print("Element not clickable.")

    @classmethod
    def click_on_element(cls, element):
        """
        Search and click on a web element.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: driver state.
        """
        try:
            return element.click()
        except TimeoutException:
            print("Element not clickable.")

    # works only with id
    # @classmethod
    # def hover_over_element(cls, locator):
    #     ActionChains(cls.driver).move_to_element(locator).perform()

    @classmethod
    def switch_frame(cls, delay, locator):
        """
        Switch driver state to another page frame.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        """
        return cls.driver.switch_to().frame(cls.wait_element_presented(delay, locator))

    @classmethod
    def wait_element_visible(cls, delay, locator):
        """
        Wait for element to be visible on the page.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return WebDriverWait(cls.driver, delay).until(EC.visibility_of_element_located((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element not visible: {}'.format(cls.__class__, e))

    @classmethod
    def wait_element_presented(cls, delay, locator):
        """
        Wait for element to be presented on the page.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return WebDriverWait(cls.driver, delay).until(EC.presence_of_element_located((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element not present: {}'.format(cls.__class__, e))

    @classmethod
    def wait_element_clickable(cls, delay, locator):
        """
        Wait for element to be clickable on the page.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return WebDriverWait(cls.driver, delay).until(EC.element_to_be_clickable((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element not clickable: {}'.format(cls.__class__, e))

    @classmethod
    def find_element(cls, locator):
        """
        find a web element without waiting.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return cls.driver.find_element_by_xpath(locator)
        except TimeoutException as e:
            print('{}: TimeoutException element not found: {}'.format(cls.__class__, e))

    @classmethod
    def find_element_by(cls, locator, by):
        """
        Find a web element by provided option.
        :param locator: xpath of a element.
        :param by: selenium option to search web element.
        :return: web element.
        """
        by = by.lower()
        try:
            if by == DriverHelper.ID.value:
                return cls.driver.find_element(By.ID, locator)
            elif by == DriverHelper.NAME.value:
                return cls.driver.find_element(By.NAME, locator)
            elif by == DriverHelper.CLASS_NAME.value:
                return cls.driver.find_element(By.CLASS_NAME, locator)
            elif by == DriverHelper.TAG_NAME.value:
                return cls.driver.find_element(By.TAG_NAME, locator)
            elif by == DriverHelper.LINK_TEXT.value:
                return cls.driver.find_element(By.LINK_TEXT, locator)
            elif by == DriverHelper.XPATH.value:
                return cls.driver.find_element(By.XPATH, locator)
            elif by == DriverHelper.CSS_SELECTOR.value:
                return cls.driver.find_element(By.CSS_SELECTOR)
            elif by == DriverHelper.PARTIAL_LINK_TEXT.value:
                return cls.driver.find_element(By.PARTIAL_LINK_TEXT, locator)
            else:
                return cls.driver.find_element(By.XPATH, locator)
        except TimeoutException as e:
            print('{}: TimeoutException element not found: {}'.format(cls.__class__, e))

    @classmethod
    def find_located_element(cls, delay, locator):
        """
        Find web element method with explicit wait.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return WebDriverWait(cls.driver, delay).until(cls.find_element(locator))
        except TimeoutException as e:
            print('{}: TimeoutException waiting for search input field: {}'.format(cls.__class__, e))

    # @classmethod
    # def if_page_loaded(cls, delay, page_elements):
    #     WebDriverWait(cls.get_driver(), delay).all_elements.get(0).get_locator_by()

    # need to change for elements
    # @classmethod
    # def print_objects_text(cls, delay, locator):
    #     element = cls.wait_element_presented(delay, locator)
    #     print(element.get_text())

    # need to change for elements
    # @classmethod
    # def get_num_of_elements(cls, locator):
    #     elements = cls.find_elements(locator)
    #     return elements.size()

    # @classmethod
    # def click_on_button(cls, locator, index):
    #     cls.find_elements(locator).get(index).click()

    # for purpose need to create check_checkbox method
    # @classmethod
    # def if_parent_element_exists(cls, delay, locator, element):
    #     cls.driver_wait(delay)
    #     result = element.find_elements(locator).size() != 0
    #     return result

    @classmethod
    def close_browser(cls):
        """
        Calling self method to close driver instance
        """
        cls.close_driver_instance()
