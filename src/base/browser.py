# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.enums import DriverHelper
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser(object):
    def go_to_url(self, driver, url):
        driver.get(url)
        driver.maximize_window()
        return self.driver_wait(driver, 3)

    def close_driver_instance(self, driver):
        driver.delete_all_cookies()
        driver.close()

    def driver_wait(self, driver, delay):
        return WebDriverWait(driver, delay)

    def get_cur_url(self, driver):
        return driver.current_url

    def get_element_span_html(self, element):
        try:
            return element.get_attribute("innerHTML")
        except TimeoutException:
            print("Element not found.")

    def highlight_element(self, driver, element):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                                  "color: green; border: 2px solid green;")
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, "")

    def get_attribute_from_locator(self, driver, locator, attribute):
        try:
            element = self.find_element(driver, locator)
            return element.get_attribute(attribute)
        except TimeoutException:
            print("Element not found.")

    def get_attribute_from_element(self, element, attribute):
        try:
            return element.get_attribute(attribute)
        except TimeoutException:
            print("Element not exists.")

    def send_keys(self, element, query):
        try:
            element.clear()
            return element.send_keys(query)
        except TimeoutException:
            print("Element not click able.")

    def send_enter_key(self, element):
        try:
            return element.send_keys(Keys.ENTER)
        except TimeoutException:
            print("Element not click able.")

    def search_element(self, driver, delay, locator):
        try:
            if self.wait_element_presented(driver, delay, locator):
                return self.wait_element_clickable(driver, delay, locator)
        except TimeoutException:
            print("Element not visible.")

    def type_text_by_locator(self, driver, delay, locator, query):
        try:
            element = self.search_element(driver, delay, locator)
            element.click()
            element.clear()
            return element.send_keys(query)
        except TimeoutException:
            print("Element not click able.")

    def click_on_element_by_locator(self, driver, delay, locator):
        try:
            element = self.wait_element_clickable(driver, delay, locator)
            return element.click()
        except TimeoutException:
            print("Element not click able.")

    def click_on_element(self, element):
        try:
            return element.click()
        except TimeoutException:
            print("Element not click able.")

    def hover_over_element_and_click(self, driver, element):
        action = ActionChains(driver)
        action.move_to_element(element)
        action.click(element)
        return action.perform()

    def click_on_captcha(self, driver, element, x, y):
        action = ActionChains(driver)
        action.move_to_element_with_offset(element, x, y)
        action.click(element)
        return action.perform()

    def switch_frame(self, driver, element):
        return driver.switch_to.window(element)

    def check_element_not_visible(self, driver, delay, locator):
        try:
            return WebDriverWait(driver, delay).until_not(EC.presence_of_element_located((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element still visible: {}'.format(self.__class__, e))

    def wait_element_visible(self, driver, delay, locator):
        try:
            return WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element not visible: {}'.format(self.__class__, e))

    def wait_element_presented(self, driver, delay, locator):
        try:
            return WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element not present: {}'.format(self.__class__, e))

    def wait_element_to_be_selected(self, driver, delay, locator):
        try:
            return WebDriverWait(driver, delay).until(EC.element_to_be_selected((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element not click able: {}'.format(self.__class__, e))

    def wait_element_clickable(self, driver, delay, locator):
        try:
            return WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element not click able: {}'.format(self.__class__, e))

    def find_element(self, driver, locator):
        try:
            return driver.find_element_by_xpath(locator)
        except TimeoutException as e:
            print('{}: TimeoutException element not found: {}'.format(self.__class__, e))

    def find_element_by(self, driver, locator, by):
        by = by.lower()
        try:
            if by == DriverHelper.ID.value:
                return driver.find_element(By.ID, locator)
            elif by == DriverHelper.NAME.value:
                return driver.find_element(By.NAME, locator)
            elif by == DriverHelper.CLASS_NAME.value:
                return driver.find_element(By.CLASS_NAME, locator)
            elif by == DriverHelper.TAG_NAME.value:
                return driver.find_element(By.TAG_NAME, locator)
            elif by == DriverHelper.LINK_TEXT.value:
                return driver.find_element(By.LINK_TEXT, locator)
            elif by == DriverHelper.CSS_SELECTOR.value:
                return driver.find_element(By.CSS_SELECTOR)
            elif by == DriverHelper.PARTIAL_LINK_TEXT.value:
                return driver.find_element(By.PARTIAL_LINK_TEXT, locator)
            else:
                return driver.find_element(By.XPATH, locator)
        except TimeoutException as e:
            print('{}: TimeoutException element not found: {}'.format(self.__class__, e))

    def close_browser(self, driver):
        self.close_driver_instance(driver)
