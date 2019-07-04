import time
import unittest
import allure
import pytest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.market_order_panel_page import MarketOrderPanelPage

test_case = '2825'


@pytest.mark.skip
@allure.title("MARKET PANEL")
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
             name='"Amount field validation" funds presentation')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/market_order_panel_tests/C2825_amount_fields_validation_test.py",
                 "TestAmountFieldsValidation")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.market_order
@pytest.mark.order_management
@ddt
class TestAmountFieldsValidation(unittest.TestCase):
    @allure.step("SetUp:  sitting new customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer.customer_registration()
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 10000)
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 3, 10)
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.market_order_panel = MarketOrderPanelPage()
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_amount_fields_validation")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_amount_fields_validation(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        result = 0
        try:
            self.assertTrue(self.home_page.open_signin_page(self.driver))
            self.assertTrue(self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password))
            assert self.browser.wait_element_presented(self.driver, self.locators.MARKET_TAB, delay)
            self.browser.execute_js(self.driver, '''$("div[class='tradeType market']").click()''')
            # for BUY
            usd_title_menu = self.browser.wait_element_presented(self.driver, self.locators.USD, delay)
            self.browser.click_on_element(usd_title_menu)
            usd_from_dropdown = self.browser.wait_element_presented(self.driver,
                                                                    self.locators.USD_OPTION_FROM_USD_DROPDOWN,
                                                                    delay)
            self.browser.click_on_element(usd_from_dropdown)
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1007]').click()''')
            input_field_buy = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_BUY, delay)
            self.browser.send_keys(input_field_buy, 'AB')
            amount_after_input_not_correct_value = self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ)
            self.assertTrue(amount_after_input_not_correct_value == '')
            query_min_order_quantity = "SELECT minOrderQuantity FROM instruments WHERE name = 'BTC/USD';"
            min_order_quantity = Instruments.run_mysql_query(query_min_order_quantity)[0][0]
            less_then_min_order_quantity = str(round(min_order_quantity - min_order_quantity / 100 * 2, 5))
            time.sleep(delay)
            available_for_trading_buy_before = self.browser.execute_js(self.driver,
                                                                       self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            input_field_buy = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_BUY, delay)
            self.browser.send_keys(input_field_buy, less_then_min_order_quantity)
            buy_button = self.browser.wait_element_presented(self.driver, self.locators.BUY_BUTTON, delay)
            self.browser.click_on_element(buy_button)
            available_for_trading_buy_after = self.browser.execute_js(self.driver,
                                                                      self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            assert available_for_trading_buy_before == available_for_trading_buy_after
            max_order_quantity = (
                Instruments.run_mysql_query("SELECT maxOrderQuantity FROM instruments WHERE name = 'BTC/USD';")[0][0])
            more_then_min_order_quantity = str(round(max_order_quantity + max_order_quantity / 100 * 2, 0))
            available_for_trading_buy_before = self.browser.execute_js(self.driver,
                                                                       self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            self.browser.send_keys(input_field_buy, more_then_min_order_quantity)
            self.browser.click_on_element(buy_button)
            available_for_trading_buy_after = self.browser.execute_js(self.driver,
                                                                      self.locators.VALUE_AVAILABLE_FOR_TRADING_BUY_JQ)
            assert available_for_trading_buy_before == available_for_trading_buy_after
            tail_digits = Instruments.run_mysql_query("SELECT tailDigits FROM currencies WHERE code = 'BTC';")[0][0]
            tail_digits_order_quantity = str(tail_digits + 1)
            more_tail_order_quantity = str(format(0.1111111111, "." + tail_digits_order_quantity + "f"))
            self.browser.send_keys(input_field_buy, more_tail_order_quantity)
            amount_after_input_tail_digit = self.browser.execute_js(self.driver, self.locators.AMOUNT_FOR_BUY_JQ)
            tail_digit_from_input = len(str(amount_after_input_tail_digit).split('.')[1])
            assert tail_digits == tail_digit_from_input
            # for SELL
            input_field_sell = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_SELL, delay)
            self.browser.send_keys(input_field_sell, 'AB')
            amount_after_input_not_correct_value_sell = self.browser.execute_js(self.driver,
                                                                                self.locators.AMOUNT_FOR_SELL_JQ)
            assert amount_after_input_not_correct_value_sell == ''
            available_for_trading_sell_before = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            input_field_sell = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_SELL, delay)
            self.browser.send_keys(input_field_sell, less_then_min_order_quantity)
            sell_button = self.browser.wait_element_presented(self.driver, self.locators.SELL_BUTTON, delay)
            self.browser.click_on_element(sell_button)
            available_for_trading_sell_after = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            assert available_for_trading_sell_before == available_for_trading_sell_after
            available_for_trading_sell_before = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            self.browser.send_keys(input_field_sell, more_then_min_order_quantity)
            self.browser.click_on_element(sell_button)
            available_for_trading_sell_after = self.browser.execute_js(
                self.driver, self.locators.VALUE_AVAILABLE_FOR_TRADING_SELL_JQ)
            assert available_for_trading_sell_before == available_for_trading_sell_after
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