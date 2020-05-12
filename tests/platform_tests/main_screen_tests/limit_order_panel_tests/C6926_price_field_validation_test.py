import time
import unittest
import allure
import pytest
from src.base import logger
from ddt import ddt, data, unpack
from config_definitions import BaseConfig
from src.base.browser import Browser
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.limit_order_panel_page import LimitOrderPanelPage

test_case = '6926'


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    UI test.
    Price field validation for Buy an Sell sections, UI
    1. Open WTP
    2. Select an instrument(1007).
    3. Insert "AB" to the "Price" field of the "Buy" section / Expected Result: amount_after_input = ''
    4. Insert "-200" to the "Price" field of the "Buy" section  / Expected Result: amount_after_input = '200'
    5. Insert value with Tail Digits more than in DB to the "Price" field of the "Buy" section  / Expected Result:
     amount_after_input has Tail Digits as set in DB.
    6. Insert "AB" to the "Price" field of the "Sell" section / Expected Result: amount_after_input = ''
    4. Insert "-200" to the "Price" field of the "Sell" section  / Expected Result: amount_after_input = '200'
    5. Insert value with Tail Digits more than in DB to the "Price" field of the "Sell" section  / Expected Result:
     amount_after_input has Tail Digits as set in DB.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Price field validation (Negative')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/limit_order_panel_tests/C6926_price_field_validation_test.py",
    "TestPriceFieldValidation")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.limit_order
@pytest.mark.order_management
@ddt
class TestPriceFieldValidation(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.limit_order_panel = LimitOrderPanelPage()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_price_field_validation(negative)")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_price_field_validation(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info(
            "method test_price_field_validation"
            "with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        delay, result = self.home_page.ui_delay, 0
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            usd_title_menu = self.browser.wait_element_presented(self.driver, self.locators.USD, delay)
            self.browser.click_on_element(usd_title_menu)
            usd_from_dropdown = self.browser.wait_element_presented(self.driver,
                                                                    self.locators.USD_OPTION_FROM_USD_DROPDOWN,
                                                                    delay)
            self.browser.click_on_element(usd_from_dropdown)
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1007]').click()''')
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 3, 10)  # BTC
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 10000)  # USD
            time.sleep(3)

            input_field_buy = self.browser.wait_element_presented(self.driver, self.locators.ENTER_PRICE_BUY, delay)
            self.browser.send_keys(input_field_buy, 'AB')
            amount_after_input_not_correct_value = self.browser.execute_js(self.driver,
                                                                           self.locators.ENTER_PRICE_BUY_JQ)
            assert amount_after_input_not_correct_value == ""

            input_field_buy = self.browser.wait_element_presented(self.driver, self.locators.ENTER_PRICE_BUY, delay)
            self.browser.send_keys(input_field_buy, '-200')
            amount_after_input_not_correct_value = self.browser.execute_js(self.driver,
                                                                           self.locators.ENTER_PRICE_BUY_JQ)
            assert amount_after_input_not_correct_value == '200'

            tail_digits = Instruments.run_mysql_query("SELECT tailDigits FROM assets WHERE name = 'BTC/USD';")[0][0]
            tail_digits_price = str(tail_digits + 1)
            more_tail_order_quantity = str(format(0.1111111111, "." + tail_digits_price + "f"))
            self.browser.send_keys(input_field_buy, more_tail_order_quantity)
            amount_after_input_tail_digit = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_BUY_JQ)
            tail_digit_from_input = len(str(amount_after_input_tail_digit).split('.')[1])
            assert tail_digits == tail_digit_from_input

            # for SELL
            input_field_sell = self.browser.wait_element_presented(self.driver, self.locators.ENTER_PRICE_SELL, delay)
            self.browser.send_keys(input_field_sell, 'AB')
            amount_after_input_not_correct_value_sell = self.browser.execute_js(self.driver,
                                                                                self.locators.ENTER_PRICE_SELL_JQ)
            assert amount_after_input_not_correct_value_sell == ''

            input_field_sell = self.browser.wait_element_presented(self.driver, self.locators.ENTER_PRICE_SELL, delay)
            self.browser.send_keys(input_field_sell, '-200')
            amount_after_input_not_correct_value_sell = self.browser.execute_js(self.driver,
                                                                                self.locators.ENTER_PRICE_SELL_JQ)
            assert amount_after_input_not_correct_value_sell == '200'

            self.browser.send_keys(input_field_sell, more_tail_order_quantity)
            amount_after_input_tail_digit = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_SELL_JQ)
            tail_digit_from_input = len(str(amount_after_input_tail_digit).split('.')[1])
            assert tail_digits == tail_digit_from_input

            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1

        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
