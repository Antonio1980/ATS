import time
import unittest
import allure
import pytest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.limit_order_panel_page import LimitOrderPanelPage

test_case = '6925'


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    UI test.
    Amount field validation, UI
    1. Open WTP
    2. Select an instrument(1007).
    3. Insert "AB" to the "Amount" field of the "Buy" section and click on the "Buy" button / Check - Order is rejected    
    4. Insert "0.0001" to the "Amount" field of the "Buy" section and click on the "Buy" button / Check -
       Order is rejected      
    5. Insert "101" to the "Amount" field of the "Buy" section and click on the "Buy" button / Check - Order is rejected    
    6. Insert a value with invalid number of digits after the decimal point for the selected instrument and click on 
       the "Buy" button / Check - Order is rejected  
    7. Insert "AB" to the "Amount" field of the "Sell" section and click on the "Buy" button / Check - Order
       is rejected    
    8. Insert "0.0001" to the "Amount" field of the "Sell" section and click on the "Buy" button / Check - Order
       is rejected      
    9. Insert "101" to the "Amount" field of the "Sell" section and click on the "Buy" button / Check - Order
       is rejected    
    10. Insert a value with invalid number of digits after the decimal point for the selected instrument and click 
       on the "Sell" button / Check - Order is rejected     
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Amount field validation (Negative)')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/limit_order_panel_tests/C6925_amount_field_validation_test.py",
                 "TestAmountFieldsValidation")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.limit_order
@pytest.mark.order_management
@ddt
class TestAmountFieldsValidation(unittest.TestCase):
    @allure.step("SetUp:  sitting new customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.customer.clean_up_customer()
        self.sign_in_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.limit_order_panel = LimitOrderPanelPage()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_amount_fields_validation")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_amount_fields_validation(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info(
            "method test_amount_fields_validation  "
            "with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        delay, result = self.home_page.ui_delay, 0
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            usd_title_menu = self.browser.wait_element_presented(self.driver, self.locators.USD, delay + 10.0)
            self.browser.click_on_element(usd_title_menu)
            usd_from_dropdown = self.browser.wait_element_presented(self.driver,
                                                                    self.locators.USD_OPTION_FROM_USD_DROPDOWN,
                                                                    delay)
            self.browser.click_on_element(usd_from_dropdown)
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1007]').click()''')
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 50000)  # USD
            self.customer.postman.balance_service.add_balance(self.customer.customer_id, 3, 10)  # BTC
            time.sleep(3)

            # for BUY
            input_buy = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_BUY, delay)
            self.browser.send_keys(input_buy, 'AB')
            amount_after_not_correct_value = self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ)
            assert amount_after_not_correct_value == ""

            query_min_order_quantity = "SELECT minOrderQuantity FROM instruments WHERE name = 'BTC/USD';"
            min_order_quantity = Instruments.run_mysql_query(query_min_order_quantity)[0][0]
            less_then_min_order_quantity = str(round(min_order_quantity - min_order_quantity / 100 * 2, 5))
            available_buy_before = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            input_buy = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_BUY, delay)
            self.browser.send_keys(input_buy, less_then_min_order_quantity)
            increases_step_button_plus_buy = self.browser.wait_element_presented(
                self.driver, self.locators.INCREASES_STEP_BUTTON_BUY, delay)
            self.browser.click_on_element(increases_step_button_plus_buy)
            buy_button = self.browser.wait_element_presented(self.driver, self.locators.BUY_BUTTON, delay)
            self.browser.click_on_element(buy_button)
            available_buy_after = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            assert available_buy_before == available_buy_after

            max_order_quantity = (Instruments.run_mysql_query("SELECT maxOrderQuantity FROM instruments WHERE name"
                                                              " = 'BTC/USD';")[0][0])
            more_then_min_order_quantity = str(round(max_order_quantity + max_order_quantity / 100 * 2, 0))
            available_buy_before = self.browser.execute_js(self.driver,
                                                           self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            self.browser.send_keys(input_buy, more_then_min_order_quantity)
            self.browser.click_on_element(buy_button)
            available_buy_after = self.browser.execute_js(self.driver,
                                                          self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            assert available_buy_before == available_buy_after

            query_tail_digits = "SELECT tailDigits FROM currencies WHERE code = 'BTC';"
            tail_digits = Instruments.run_mysql_query(query_tail_digits)[0][0]
            tail_digits_order_quantity = str(tail_digits + 1)
            more_tail_order_quantity = str(format(0.1111111111, "." + tail_digits_order_quantity + "f"))
            self.browser.send_keys(input_buy, more_tail_order_quantity)
            amount_after_input_tail_digit = self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ)
            tail_digit_from_input = len(str(amount_after_input_tail_digit).split('.')[1])
            assert tail_digits == tail_digit_from_input

            # for SELL
            input_field_sell = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_SELL, delay)
            self.browser.send_keys(input_field_sell, 'AB')
            amount_after_input_not_correct_value_sell = self.browser.execute_js(self.driver,
                                                                                self.locators.AMOUNT_FOR_SELL_JQ)
            assert amount_after_input_not_correct_value_sell == ''

            available_sell_before = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            input_field_sell = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_SELL, delay)
            self.browser.send_keys(input_field_sell, less_then_min_order_quantity)
            increases_step_button_plus_sell = self.browser.wait_element_presented(
                self.driver, self.locators.INCREASES_STEP_BUTTON_SELL, delay)
            self.browser.click_on_element(increases_step_button_plus_sell)
            sell_button = self.browser.wait_element_presented(self.driver, self.locators.SELL_BUTTON, delay)
            self.browser.click_on_element(sell_button)
            available_sell_after = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            assert available_sell_before == available_sell_after

            available_sell_before = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            self.browser.send_keys(input_field_sell, more_then_min_order_quantity)
            self.browser.click_on_element(sell_button)
            available_sell_after = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            assert available_sell_before == available_sell_after

            self.browser.send_keys(input_field_sell, more_tail_order_quantity)
            amount_after_input_tail_digit = self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_SELL_JQ)
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
