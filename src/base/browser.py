import time
from src.base.enums import DriverHelper
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Browser(object):
    def go_to_url(self, driver, url):
        """
        Browse the given url by passed driver instance.
        :param driver: web_driver instance.
        :param url: string url to browse.
        :return: browser state with wed driver explicit wait.
        """
        driver.get(url)
        return driver.maximize_window()

    def close_driver_instance(self, driver):
        """
        Deletes all cookies and closes web driver instance.
        :param driver: web_driver instance.
        """
        driver.delete_all_cookies()
        driver.close()
        driver.quit()

    def close_browser(self, driver):
        """
        Calling self method to close driver instance.
        """
        self.close_driver_instance(driver)

    def driver_wait(self, driver, delay=+1):
        """
        Explicit wait for given driver with delay.
        :param delay: seconds to wait.
        :param driver: web_driver instance.
        :return: web_driver state.
        """
        return WebDriverWait(driver, delay)

    def wait_driver(self, driver, delay=+1):
        """
        Implicit wait for given driver with delay.
        :param delay: seconds to wait.
        :param driver: web_driver instance.
        :return: web_driver state.
        """
        return driver.implicitly_wait(delay)

    def get_cur_url(self, driver):
        """
        Get the url from browser state.
        :param driver: web_driver instance.
        :return: current url from browser.
        """
        return driver.current_url

    def get_element_span_html(self, element):
        """
        Get attribute text of a web element.
        :param element: web element.
        :return: span tag of a web element.
        """
        try:
            return element.get_attribute("innerHTML")
        except Exception as e:
            print("{0} Element not found. {0}").format(self.__class__, e)

    def highlight_element(self, driver, element):
        """
        To highlight web element using script.
        :param driver: web_driver instance.
        :param element: Web element.
        """
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                              "color: green; border: 2px solid green;")
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, "")

    def get_attribute_from_locator(self, driver, locator, attribute):
        """
        Get attribute text of a web element by locator.
        :param driver: web_driver instance.
        :param locator: locator string.
        :param attribute: attribute string.
        :return:
        """
        try:
            element = self.find_element(driver, locator)
            return element.get_attribute(attribute)
        except Exception as e:
            print("{0} Element not found. {0}").format(self.__class__, e)

    def get_attribute_from_element(self, element, attribute):
        """
        Get attribute text of a web element.
        :param element: web element.
        :param attribute: attribute string.
        :return: span tag of a web element.
        """
        try:
            return element.get_attribute(attribute)
        except Exception as e:
            print("{0} Element not exists. {0}").format(self.__class__, e)

    def send_keys(self, element, query):
        """
        Clear and type a text into web element.
        :param element: web element.
        :param query: text to type.
        :return: driver state.
        """
        try:
            element.clear()
            return element.send_keys(query)
        except Exception as e:
            print("{0} Element not click able.").format(self.__class__, e)

    def send_enter_key(self, element):
        """
        Push the enter key on web element.
        :param element: web element.
        :return: driver state.
        """
        try:
            return element.send_keys(Keys.ENTER)
        except Exception as e:
            print("{0} Element not click able. {0}").format(self.__class__, e)

    def execute_js(self, driver, script, *args):
        """
        Injection js code into current driver state.
        :param driver: web_driver instance.
        :param script: java script code passed as string.
        """
        return driver.execute_script(script, args)

    def drag_and_drop(self, driver, source_element, destination_element):
        """
        Drags and drops a web element.
        :param driver: web_driver instance.
        :param source_element: web element to drag.
        :param destination_element: web element to drop to.
        """
        ActionChains(driver).drag_and_drop(source_element, destination_element).perform()

    def search_element(self, driver, locator, delay):
        """
        Search a web element on a page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return self.driver_wait(driver, delay).until(lambda x: x.find_element_by_xpath(locator))
        except Exception as e:
            print("{0} Element not found. {0}").format(self.__class__, e)

    def type_text_by_locator(self, driver, locator, query):
        """
        Clear and type text into web element.
        :param driver: web_driver instance.
        :param locator: xpath of a element.
        :param query: text to type.
        :return: driver state.
        """
        delay = 5
        try:
            element = self.search_element(driver, locator, delay)
            element.click()
            element.clear()
            element.send_keys(query)
            return self.send_enter_key(element)
        except Exception as e:
            print("{0} Element not click able. {0}").format(self.__class__, e)

    def click_on_element_by_locator(self, driver, locator, delay=+1):
        """
        Wait, search by locator and click on a web element.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: driver state.
        """
        try:
            element = self.wait_element_clickable(driver, locator, delay)
            element.click()
        except Exception as e:
            print("{0} Element not click able. {0}").format(self.__class__, e)

    def click_on_element(self, element):
        """
        Click on a passed web element.
        :param element: web element.
        :return: driver state.
        """
        try:
            element.click()
        except Exception as e:
            print("{0} Element not click able. {0}").format(self.__class__, e)

    def choose_option_from_dropdown(self, driver, dropdown_locator, dropdown_field_locator, dropdown_option, delay=1):
        """
        Searches for web elements (drop-down and text-input) and selects option from drop-down.
        :param driver: web_driver instance.
        :param dropdown_locator: string locator for drop-down.
        :param dropdown_field_locator: string locator for text-input.
        :param dropdown_option: option to select from drop-down.
        :param delay: delay to wait between actions.
        """
        dropdown = self.find_element(driver, dropdown_locator)
        dropdown_field = self.find_element(driver, dropdown_field_locator)
        action = Actions(driver)
        action.click(dropdown)
        action.wait(delay)
        action.click(dropdown_field)
        action.wait(delay)
        action.send_keys(dropdown_option)
        action.wait(delay)
        action.send_keys(Keys.ENTER)
        return action.perform()

    def hover_over_element_and_click(self, driver, element):
        """
        Hover over web element and clicks on it.
        :param driver: web_driver instance.
        :param element: web element.
        :return: browser state with performed actions.
        """
        action = ActionChains(driver)
        action.move_to_element(element)
        action.click(element)
        return action.perform()

    def click_with_offset(self, driver, element, x, y):
        """
        Clicks on web element with x.y coordinates.
        :param y: vertical coordinate in pixels.
        :param x: horizontal coordinate in pixels.
        :param driver: web_driver instance.
        :param element: web element.
        :return: browser state with performed actions.
        """
        action = ActionChains(driver)
        action.move_to_element_with_offset(element, x, y)
        action.click(element)
        return action.perform()

    def click_with_wait_and_offset(self, driver, element, x, y, delay):
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

    def click_and_wait(self, driver, element, delay=1):
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
        return action.perform()

    def switch_frame(self, driver, element):
        """
        Switch current frame to another page frame.
        :param driver: web_driver instance.
        :param element: web element.
        :return: driver state on switched frame.
        """
        return driver.switch_to.frame(element)

    def switch_window(self, driver, element):
        """
        Switch current browser window to another window.
        :param driver: web_driver instance.
        :param element: web element.
        :return: driver state on switched frame.
        """
        return driver.switch_to.window(element)

    def wait_for_new_window(self, driver, delay=5):
        """
        Waits and checks if another window is open.
        :param driver: web_driver instance.
        :param delay: seconds to wait.
        :return: True if additional window is open and False otherwise. 
        """
        handles_before = driver.window_handles
        yield
        return self.driver_wait(driver, delay).until(
            lambda driver: len(handles_before) != len(driver.window_handles))

    def refresh_page(self, driver):
        """
        Refresh browser page by sending 'Ctrl + r' keys.
        :param driver: web_driver instance.
        """
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')

    def refresh_browser(self, driver):
        """
        Refresh browser by navigating on 'refresh' button.
        :param driver: web_driver instance.
        """
        driver.navigate().refresh()

    def back_browser(self, driver):
        """
        To go back on previous page using driver.
        :param driver: web_driver instance.
        """
        driver.navigate().back()

    def forward_browser(self, driver):
        """
        To go forward on previous page using driver.
        :param driver: web_driver instance.
        """
        driver.navigate().forward()

    def go_back(self, driver):
        """
        To go back on previous page using js.
        :param driver: web_driver instance.
        """
        driver.execute_script("window.history.go(-1)")

    def check_element_not_visible(self, driver, locator, delay=+1):
        """
        Wait and check than element not visible on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: True if matches condition and False otherwise.
        """
        try:
            return self.driver_wait(driver, delay).until_not(ec.visibility_of_element_located((By.XPATH, locator)))
        except Exception as e:
            print('{}: TimeoutException element still visible: {}'.format(self.__class__, e))

    def check_element_not_presented(self, driver, locator, delay=+1):
        """
        Wait and check than element not present on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: True if matches condition and False otherwise.
        """
        try:
            return self.driver_wait(driver, delay).until_not(ec.presence_of_element_located((By.XPATH, locator)))
        except Exception as e:
            print('{}: TimeoutException element still present: {}'.format(self.__class__, e))

    def check_element_to_not_be_selected(self, driver, locator, delay=+1):
        """
        Wait for element to be click able on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: True if matches condition and False otherwise.
        """
        try:
            return self.driver_wait(driver, delay).until_not(ec.element_to_be_selected((By.XPATH, locator)))
        except Exception as e:
            print('{}: TimeoutException element still can be selected: {}'.format(self.__class__, e))

    def wait_number_of_windows(self, driver, number, delay=+1):
        """
        Waits for new window to be opened.
        :param driver: web_driver instance.
        :param number: number of expected window opened.
        :param delay: seconds to wait an element.
        :return: True if matches condition and False otherwise.
        """
        try:
            return self.driver_wait(driver, delay).until(ec.number_of_windows_to_be(number))
        except Exception as e:
            print('{}: TimeoutException element not visible: {}'.format(self.__class__, e))

    def wait_url_contains(self, driver, _url, delay=+1):
        """
        Waits and checks if expected url is contains to current url.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param _url: expected url. 
        :return: True if matches condition and False otherwise.
        """
        try:
            return self.driver_wait(driver, delay).until(ec.url_contains(_url))
        except Exception as e:
            print('{}: TimeoutException element not visible: {}'.format(self.__class__, e))

    def wait_url_matches(self, driver, _url, delay=+1):
        """
        Waits and checks if expected url is matches to current url.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param _url: expected url.
        :return: True if matches condition and False otherwise.
        """
        try:
            return self.driver_wait(driver, delay).until(ec.url_matches(_url))
        except Exception as e:
            print('{}: TimeoutException element not visible: {}'.format(self.__class__, e))

    def wait_element_visible(self, driver, locator, delay=+1):
        """
        Wait for element to be visible on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return self.driver_wait(driver, delay).until(ec.visibility_of_element_located((By.XPATH, locator)))
        except Exception as e:
            print('{}: TimeoutException element not visible: {}'.format(self.__class__, e))

    def wait_element_presented(self, driver, locator, delay=+1):
        """
        Wait for element to be presented on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return self.driver_wait(driver, delay).until(ec.presence_of_element_located((By.XPATH, locator)))
        except Exception as e:
            print('{}: TimeoutException element not present: {}'.format(self.__class__, e))

    def wait_element_to_be_selected(self, driver, locator, delay=+1):
        """
        Wait for element to be click able on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return self.driver_wait(driver, delay).until(ec.element_to_be_selected((By.XPATH, locator)))
        except Exception as e:
            print('{}: TimeoutException element cant be selected: {}'.format(self.__class__, e))

    def wait_element_clickable(self, driver, locator, delay=+1):
        """
        Wait for element to be click able on the page.
        :param driver: web_driver instance.
        :param delay: seconds to wait an element.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return self.driver_wait(driver, delay).until(ec.element_to_be_clickable((By.XPATH, locator)))
        except Exception as e:
            print('{}: TimeoutException element not click able: {}'.format(self.__class__, e))

    def find_element(self, driver, locator):
        """
        Find a web element without waiting by locator.
        :param driver: web_driver instance.
        :param locator: xpath of a element.
        :return: web element.
        """
        try:
            return driver.find_element_by_xpath(locator)
        except Exception as e:
            print('{}: TimeoutException element not found: {}'.format(self.__class__, e))

    def find_element_by(self, driver, locator, by):
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
        except Exception as e:
            print('{}: TimeoutException element not found: {}'.format(self.__class__, e))

    def select_by_value(self, element, value):
        """
        Select option from selector by value.
        :param element: selector web element.
        :param value: value for option to select.
        """
        if value is not str:
            value = str(value)
        selector = Select(element)
        selector.select_by_value(value)

    def select_by_index(self, element, index):
        """
        Select option from selector by index.
        :param element: selector web element.
        :param index: value for option to select.
        """
        if index is not int:
            index = int(index)
        selector = Select(element)
        selector.select_by_index(index)

    def find_elements(self, driver, locator):
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
        except TimeoutError as e:
            print('{}: TimeoutException element not found: {}'.format(self.__class__, e))


    # def if_page_loaded(self, delay, page_elements):
    #     WebDriverWait(self.get_driver(), delay).all_elements.get(0).get_locator_by()

    # need to change for elements
    # def print_objects_text(self, delay, locator):
    #     element = self.wait_element_presented(delay, locator)
    #     print(element.get_text())

    # need to change for elements
    # def get_num_of_elements(self, locator):
    #     elements = self.find_elements(locator)
    #     return elements.size()

    # def click_on_button(self, locator, index):
    #     self.find_elements(locator).get(index).click()

    # for purpose need to create check_checkbox method
    # def if_parent_element_exists(self, delay, locator, element):
    #     self.driver_wait(delay)
    #     result = element.find_elements(locator).size() != 0
    #     return result


class Actions(ActionChains):
    def wait(self, delay: float):
        self._actions.append(lambda: time.sleep(delay))
        return self
    