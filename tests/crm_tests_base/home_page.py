from src.base import logger
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.base_page import BasePage
from selenium.webdriver.remote.webelement import WebElement
from tests.crm_tests_base.locators import home_page_locators
from tests.crm_tests_base import home_page_url, user_management_page_url


class HomePage(BasePage):

    def __init__(self):
        super(HomePage, self).__init__()
        self.locators = home_page_locators
        self.customer_id_locator = "//*[@class='customerIdtext'][contains(text(),'Customer ID {0}')]"

        self.script_get_val = '''return $("span[class='customerIdtext']").text();'''

    @automation_logger(logger)
    def logout(self, driver):
        self.ui_delay = self.ui_delay
        try:
            assert self.find_element_by(driver, self.locators.HOME_PAGE_LOGO_ID, "id")
            self.click_on_element_by_locator(driver, self.locators.SETTINGS_DROPDOWN, self.ui_delay)
            self.click_on_element_by_locator(driver, self.locators.LANGUAGE_ICON, self.ui_delay)
            self.click_on_element_by_locator(driver, self.locators.LOGOUT_LINK, self.ui_delay)
            return isinstance(self.wait_element_presented(driver, self.base_locators.CRM_LOGO, self.ui_delay), WebElement)
        except Exception as e:
            logger.logger.error("{0} check_balance failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    @automation_logger(logger)
    def choose_customer_by_option(self, driver, customer, option):
        customer_option = None
        try:
            # assert self.wait_url_contains(driver, home_page_url, self.ui_delay)
            customer_field = self.find_element(driver, self.locators.CUSTOMER_DROPDOWN)
            self.click_on_element(customer_field)
            if option == "Id":
                customer_option = self.find_element(driver, self.locators.CUSTOMER_ID_OPTION)
            elif option == "Name":
                customer_option = self.find_element(driver, self.locators.CUSTOMER_NAME_OPTION)
            elif option == "Email":
                customer_option = self.find_element(driver, self.locators.CUSTOMER_EMAIL_OPTION)
            if customer_option is not None:
                self.click_on_element(customer_option)
            customer_name_field = self.find_element_by(driver, self.locators.CUSTOMER_NAME_FIELD_ID, "id")
            self.click_on_element(customer_field)
            self.send_keys(customer_name_field, customer)
            show_button = self.find_element_by(driver, self.locators.SHOW_RESULTS_BUTTON_ID, "id")
            self.click_on_element(show_button)
            self.wait_number_of_windows(driver, 2, self.ui_delay)
            new_window = driver.window_handles[1]
            self.switch_window(driver, new_window)
            return self.wait_url_contains(driver, str(customer), self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} choose_customer_by_option failed with error: {1}".format(e.__class__.__name__,
                                                                                              e.__cause__))
            raise e

    @automation_logger(logger)
    def go_to_management_inset_with_users_option(self, driver):
        try:
            assert self.wait_url_contains(driver, home_page_url, self.ui_delay)
            self.choose_option_from_dropdown(driver, self.locators.MANAGEMENT_DROPDOWN,
                                             self.locators.MANAGEMENT_USERS_OPTION, "")
            return self.wait_url_contains(driver, user_management_page_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} go_to_management_inset_with_users_option failed with error: {1}".format(
                e.__class__.__name__, e.__cause__))
            return False
