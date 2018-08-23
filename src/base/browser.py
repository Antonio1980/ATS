"""
Author: Anton Shipulin.
Created: 01.08.2018
Version: 1.05
"""

import time
from src.base.enums import DriverHelper
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec


class Browser:
    @classmethod
    def go_to_url(cls, driver, url):
        """
        Browse the given url by passed driver instance.
        :param driver: web_driver instance.
        :param url: string url to browse.
        :return: browser state with wed driver explicit wait.
        """
        driver.get(url)
        return driver.maximize_window()

    @classmethod
    def close_driver_instance(cls, driver):
        """
        Deletes all cookies and closes web driver instance.
        :param driver: web_driver instance.
        """
        driver.delete_all_cookies()
        driver.close()
        driver.quit()

    @classmethod
    def driver_wait(cls, driver, delay=+1):
        """
        Explicit wait for given driver with delay.
        :param delay: seconds to wait.
        :param driver: web_driver instance.
        :return: web_driver state.
        """
        return WebDriverWait(driver, delay)

    @classmethod
    def wait_driver(cls, driver, delay):
        """
        Implicit wait for given driver with delay.
        :param delay: seconds to wait.
        :param driver: web_driver instance.
        :return: web_driver state.
        """
        return driver.implicitly_wait(delay)

    @classmethod
    def get_cur_url(cls, driver):
        """
        Get the url from browser state.
        :param driver: web_driver instance.
        :return: current url from browser.
        """
        return driver.current_url

    @classmethod
    def get_element_span_html(cls, element):
        """
        Get the innerHTML attribute value from a web element.
        :param element: web element.
        :return: string value of the innerHTML attribute.
        """
        return element.get_attribute("innerHTML")

    @classmethod
    def highlight_element(cls, driver, element):
        """
        To highlight web element using script.
        :param driver: web_driver instance.
        :param element: Web element.
        """
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                              "color: green; border: 2px solid green;")
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, "")

    @classmethod
    def get_attribute_from_element(cls, element, attribute):
        """
        Get attribute text of a web element.
        :param element: web element.
        :param attribute: attribute string.
        :return: attribute value.
        """
        return element.get_attribute(attribute)

    @classmethod
    def send_enter_key(cls, element):
        """
        Clicks on 'ENTER' button for given web element.
        :param element: web element.
        """
        element.send_keys(Keys.ENTER)

    @classmethod
    def execute_js(cls, driver, script, *args):
        """
        Injection js code into current driver state.
        :param args: tuple of additional parameters.
        :param driver: web_driver instance.
        :param script: java script code passed as string.
        :return: result of the script execution.
        """
        return driver.execute_script(script, args)

    @classmethod
    def drag_and_drop(cls, driver, source_element, destination_element):
        """
        Drags and drops a web element.
        :param driver: web_driver instance.
        :param source_element: web element to drag.
        :param destination_element: web element to drop to.
        :return: web driver state.
        """
        return Actions(driver).drag_and_drop(source_element, destination_element).perform()

    @classmethod
    def hover_over_element_and_click(cls, driver, element):
        """
        Hover over web element and clicks on it.
        :param driver: web_driver instance.
        :param element: web element.
        :return: browser state with performed actions.
        """
        action = Actions(driver)
        action.move_to_element(element)
        action.click(element)
        return action.perform()

    @classmethod
    def click_with_offset(cls, driver, element, x, y):
        """
        Clicks on web element with x.y coordinates.
        :param y: vertical coordinate in pixels.
        :param x: horizontal coordinate in pixels.
        :param driver: web_driver instance.
        :param element: web element.
        :return: browser state with performed actions.
        """
        action = Actions(driver)
        action.move_to_element_with_offset(element, x, y)
        action.click(element)
        return action.perform()

    @classmethod
    def click_with_wait_and_offset(cls, driver, element, x, y, delay):
        """
        Waits and clicks on web element with x.y coordinates.
        :param driver: web_driver instance.
        :param element: web element.
        :param x: horizontal coordinate in pixels.
        :param y: vertical coordinate in pixels.
        :param delay: seconds to wait.
        :return: browser state with performed actions.
        """
        action = Actions(driver)
        action.move_to_element_with_offset(element, x, y)
        action.wait(delay)
        action.click(element)
        return action.perform()

    @classmethod
    def try_click(cls, driver, element, delay=1):
        """
        Clicks with time delay between actions.
        :param driver: web_driver instance.
        :param element: web element.
        :param delay: seconds to wait.
        :return: browser state with performed actions.
        """
        action = Actions(driver)
        action.move_to_element(element)
        action.wait(delay)
        action.click(element)
        action.wait(delay)
        return action.perform()

    @classmethod
    def switch_frame(cls, driver, element):
        """
        Switch current frame to another page frame.
        :param driver: web_driver instance.
        :param element: web element.
        :return: driver state on switched frame.
        """
        return driver.switch_to.frame(element)

    @classmethod
    def switch_window(cls, driver, element):
        """
        Switch current browser window to another window.
        :param driver: web_driver instance.
        :param element: web element.
        :return: driver state on switched frame.
        """
        return driver.switch_to.window(element)

    @classmethod
    def refresh_page(cls, driver):
        """
        Refresh browser page by sending 'Ctrl + r' keys.
        :param driver: web_driver instance.
        """
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')

    @classmethod
    def refresh_browser(cls, driver):
        """
        Refresh browser by navigating on 'refresh' button.
        :param driver: web_driver instance.
        """
        driver.navigate().refresh()

    @classmethod
    def back_browser(cls, driver):
        """
        To go back on previous page using driver.
        :param driver: web_driver instance.
        """
        driver.navigate().back()

    @classmethod
    def forward_browser(cls, driver):
        """
        To go forward on previous page using driver.
        :param driver: web_driver instance.
        """
        driver.navigate().forward()

    @classmethod
    def go_back(cls, driver):
        """
        To go back on previous page using js.
        :param driver: web_driver instance.
        """
        driver.execute_script("window.history.go(-1)")

    @classmethod
    def select_by_value(cls, element, value):
        """
        Select option from selector by value.
        :param element: selector web element.
        :param value: value for option to select.
        """
        if value is not str:
            value = str(value)
        selector = Select(element)
        selector.select_by_value(value)

    @classmethod
    def select_by_index(cls, element, index):
        """
        Select option from selector by index.
        :param element: selector web element.
        :param index: value for option to select.
        """
        if index is not int:
            index = int(index)
        selector = Select(element)
        selector.select_by_index(index)

    @classmethod
    def close_browser(cls, driver):
        """
        Calling cls method to close driver instance.
        """
        cls.close_driver_instance(driver)

    @classmethod
    def send_keys(cls, element, query):
        """
        Clear and type a text into web element.
        :param element: web element.
        :param query: text to type.
        """
        try:
            element.clear()
            element.send_keys(query)
        except Exception as e:
            print("{0} Send keys method failed with error.").format(cls.__class__, e)

    @classmethod
    def get_attribute_from_locator(cls, driver, locator, attribute):
        """
        Get attribute text of a web element by locator.
        :param driver: web_driver instance.
        :param locator: locator string.
        :param attribute: attribute string.
        :return: attribute value.
        """
        try:
            element = cls.find_element(driver, locator)
            return element.get_attribute(attribute)
        except TimeoutException as e:
            print("{0} Element not found. {0}").format(cls.__class__, e)

    @classmethod
    def search_element(cls, driver, locator, delay):
        """
        Search a web element on a page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return cls.driver_wait(driver, delay).until(lambda x: x.find_element_by_xpath(locator))
        except TimeoutException as e:
            print("{0} Element not found. {0}").format(e.__context__)

    @classmethod
    def type_text_by_locator(cls, driver, locator, query):
        """
        Clear and type text into web element.
        :param driver: web_driver instance.
        :param locator: xpath of a element.
        :param query: text to type.
        """
        delay = 5
        try:
            element = cls.search_element(driver, locator, delay)
            element.click()
            element.clear()
            element.send_keys(query)
            cls.send_enter_key(element)
        except Exception as e:
            print("{0} Element not click able. {0}").format(cls.__class__, e)

    @classmethod
    def wait_for_new_window(cls, driver, delay=5):
        """
        Waits and checks if another window is open.
        :param driver: web_driver instance.
        :param delay: seconds to wait.
        :return: True if additional window is open and False otherwise.
        """
        handles_before = driver.window_handles
        yield
        try:
            return cls.driver_wait(driver, delay).until(
                lambda d: len(handles_before) != len(driver.window_handles))
        except TimeoutException as e:
            print("{0} Window not found. {0}").format(e.__context__)

    @classmethod
    def click_on_element_by_locator(cls, driver, locator, delay=+1):
        """
        Wait, search by locator and click on a web element.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        """
        try:
            element = cls.wait_element_clickable(driver, locator, delay)
            element.click()
        except TimeoutException as e:
            print("{0} Element not click able. {0}").format(cls.__class__, e)

    @classmethod
    def click_on_element(cls, element):
        """
        Click on a passed web element.
        :param element: web element.
        """
        try:
            element.click()
        except Exception as e:
            print("{0} Element not click able. {0}").format(cls.__class__, e)

    @classmethod
    def choose_option_from_dropdown(cls, driver, dropdown_locator, dropdown_field_locator, dropdown_option, delay=1):
        """
        Searches for web elements (drop-down and text-input) and selects option from drop-down.
        :param driver: web_driver instance.
        :param dropdown_locator: string locator for drop-down.
        :param dropdown_field_locator: string locator for text-input.
        :param dropdown_option: option to select from drop-down.
        :param delay: delay to wait between actions.
        :return: driver state with performed actions.
        """
        dropdown = cls.find_element(driver, dropdown_locator)
        if isinstance(dropdown_field_locator, WebElement):
            dropdown_field = dropdown_field_locator
        else:
            dropdown_field = cls.find_element(driver, dropdown_field_locator)
        action = Actions(driver)
        action.click(dropdown)
        action.wait(delay)
        action.click(dropdown_field)
        action.wait(delay)
        action.send_keys(dropdown_option)
        action.wait(delay)
        action.send_keys(Keys.ENTER)
        return action.perform()

    @classmethod
    def check_element_not_visible(cls, driver, locator, delay=+1):
        """
        Wait and check than element not visible on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: True if matches condition and False otherwise.
        """
        try:
            return cls.driver_wait(driver, delay).until_not(ec.visibility_of_element_located((By.XPATH, locator)))
        except Exception as e:
            print('{}: TimeoutException element still visible: {}'.format(cls.__class__, e))

    @classmethod
    def check_element_not_presented(cls, driver, locator, delay=+1):
        """
        Wait and check than element not present on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: True if matches condition and False otherwise.
        """
        try:
            return cls.driver_wait(driver, delay).until_not(ec.presence_of_element_located((By.XPATH, locator)))
        except Exception as e:
            print('{}: TimeoutException element still present: {}'.format(cls.__class__, e))

    @classmethod
    def check_element_to_not_be_selected(cls, driver, locator, delay=+1):
        """
        Wait for element to be click able on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: True if matches condition and False otherwise.
        """
        try:
            return cls.driver_wait(driver, delay).until_not(ec.element_to_be_selected((By.XPATH, locator)))
        except Exception as e:
            print('{}: TimeoutException element still can be selected: {}'.format(cls.__class__, e))

    @classmethod
    def wait_number_of_windows(cls, driver, number, delay=+1):
        """
        Waits for new window to be opened.
        :param driver: web_driver instance.
        :param number: number of expected window opened.
        :param delay: seconds to wait an element.
        :return: True if matches condition and False otherwise.
        """
        try:
            return cls.driver_wait(driver, delay).until(ec.number_of_windows_to_be(number))
        except TimeoutException as e:
            print('{}: Expected window not found: {}'.format(cls.__class__, e))

    @classmethod
    def wait_url_contains(cls, driver, _url, delay=+1):
        """
        Waits and checks if expected url is contains to current url.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param _url: expected url.
        :return: True if matches condition and False otherwise.
        """
        try:
            return cls.driver_wait(driver, delay).until(ec.url_contains(_url))
        except TimeoutException as e:
            print('{}: TimeoutException expected url not found: {}'.format(cls.__class__, e))

    @classmethod
    def wait_url_matches(cls, driver, _url, delay=+1):
        """
        Waits and checks if expected url is matches to current url.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param _url: expected url.
        :return: True if matches condition and False otherwise.
        """
        try:
            return cls.driver_wait(driver, delay).until(ec.url_matches(_url))
        except TimeoutException as e:
            print('{}: TimeoutException expected url not matches: {}'.format(cls.__class__, e))

    @classmethod
    def wait_element_visible(cls, driver, locator, delay=+1):
        """
        Wait for element to be visible on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return cls.driver_wait(driver, delay).until(ec.visibility_of_element_located((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element not visible: {}'.format(cls.__class__, e))

    @classmethod
    def wait_element_presented(cls, driver, locator, delay=+1):
        """
        Wait for element to be presented on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return cls.driver_wait(driver, delay).until(ec.presence_of_element_located((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element not present: {}'.format(cls.__class__, e))

    @classmethod
    def wait_element_to_be_selected(cls, driver, locator, delay=+1):
        """
        Wait for element to be click able on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return cls.driver_wait(driver, delay).until(ec.element_to_be_selected((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element cant be selected: {}'.format(cls.__class__, e))

    @classmethod
    def wait_element_clickable(cls, driver, locator, delay=+1):
        """
        Wait for element to be click able on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return cls.driver_wait(driver, delay).until(ec.element_to_be_clickable((By.XPATH, locator)))
        except TimeoutException as e:
            print('{}: TimeoutException element not click able: {}'.format(cls.__class__, e))

    @classmethod
    def find_element(cls, driver, locator):
        """
        Find a web element without waiting by locator.
        :param driver: web_driver instance.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return driver.find_element_by_xpath(locator)
        except TimeoutException as e:
            print('{}: TimeoutException element not found: {}'.format(cls.__class__, e))

    @classmethod
    def find_element_by(cls, driver, locator, by):
        """
        Find a web element by provided option.
        :param driver: web_driver instance.
        :param locator: xpath of a element.
        :param by: selenium option to search web element.
        :return: web element.
        """
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
            print('{}: TimeoutException element not found: {}'.format(cls.__class__, e))

    @classmethod
    def find_elements(cls, driver, locator):
        """
        Find all duplicated elements in a DOM.
        :param driver: web_driver instance.
        :param locator: selector web element.
        :return: list of web elements.
        """
        elements = []
        try:
            for i in driver.find_elements_by_xpath(locator):
                elements.append(i)
            return elements
        except TimeoutException as e:
            print('{}: TimeoutException element not found: {}'.format(cls.__class__, e))

    # def if_page_loaded(cls, delay, page_elements):
    #     WebDriverWait(cls.get_driver(), delay).all_elements.get(0).get_locator_by()

    # need to change for elements
    # def print_objects_text(cls, delay, locator):
    #     element = cls.wait_element_presented(delay, locator)
    #     print(element.get_text())

    # need to change for elements
    # def get_num_of_elements(cls, locator):
    #     elements = cls.find_elements(locator)
    #     return elements.size()

    # def click_on_button(cls, locator, index):
    #     cls.find_elements(locator).get(index).click()

    # for purpose need to create check_checkbox method
    # def if_parent_element_exists(cls, delay, locator, element):
    #     cls.driver_wait(delay)
    #     result = element.find_elements(locator).size() != 0
    #     return result


class Actions(ActionChains):
    def wait(self, delay: float):
        self._actions.append(lambda: time.sleep(delay))
        return self
