import time
import unittest
import allure
import pytest
from src.base import logger
from ddt import ddt, unpack, data
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.market_order_panel_page import MarketOrderPanelPage

test_case = '2831'


@pytest.mark.skip
@allure.title("MARKET PANEL")
@allure.description("""
    UI test.
    Verified that Estimate Price is calculated per amount in "Sell" section, UI
    1. Open WTP
    2. Select an instrument(1032).
    3. Enter a new "quoted" currency amount ("Sell" section). It must be smaller than the quantity of the first order 
       from Order Book.
    4. Check that the "Estimate Price" presented is equals to the price of the first order from Order Book
    5. Enter a new "quoted" currency amount ("Sell" section). It must be equal to a sum of the first and half of 
       the second orders quantities from Order Book.
    6. Check that the "Estimate Price" equals to the average price of the first 2 orders from Order Book calculated 
       according to their quantity
    7. Enter a new "quoted" currency amount ("Sell" section). It must be equal to a sum of the first and the second
       orders quantities from  Order Book
    8. Check that the "Estimate Price" presented is equals to the average price of the first two orders from Order Book
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Sell" section - Estimate Price is calculated per amount')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/market_order_panel_tests/C2831_sell_estimate_price_calculation_amount_test.py",
                 "TestSellEstimatePriceCalculationAmount")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.market_order
@pytest.mark.order_management
@ddt
class TestSellEstimatePriceCalculationAmount(unittest.TestCase):
    @allure.step("SetUp:  calling registered customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.market_order_panel = MarketOrderPanelPage()
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 4, 200000)  # ETH crypto
        self.locators = self.market_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_sell_estimate_price_calculation_amount")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_sell_estimate_price_calculation_amount(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        result = 0
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            assert self.browser.wait_element_presented(self.driver, self.locators.MARKET_TAB, delay)
            self.browser.execute_js(self.driver, '''$("div[class='tradeType market']").click()''')
            usd_title_menu = self.browser.wait_element_presented(self.driver, self.locators.USD, delay)
            self.browser.click_on_element(usd_title_menu)
            jpy_from_dropdown = self.browser.wait_element_presented(self.driver,
                                                                    self.locators.JPY_OPTION_FROM_USD_DROPDOWN, delay)
            self.browser.click_on_element(jpy_from_dropdown)
            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1032]').click()''')
            assert self.browser.wait_element_presented(self.driver,
                                                       self.locators.ETH_JPY_TITLE_ON_INSTRUMENT_QUICK_INFO_PANEL,
                                                       delay + 5)
            best_price_and_quantity = Instruments.get_orders_best_price_and_quantity(1032, "sell", 2)[:50]
            quantity = best_price_and_quantity[0][1]
            price = best_price_and_quantity[0][0]
            second_quantity = best_price_and_quantity[1][1]
            second_price = best_price_and_quantity[1][0]
            enter_amount_sell = self.browser.wait_element_presented(self.driver, self.locators.AMOUNT_FOR_SELL, delay)
            order_quantity_one = str(round(quantity - (quantity / 100 * 20), 5))
            self.browser.send_keys(enter_amount_sell, order_quantity_one)
            expected_price_one = str(int(price))
            time.sleep(2)
            estimated_price_sell_one = self.browser.execute_js(self.driver, self.locators.ESTIMATED_PRICE_FOR_SELL_JQ)
            assert expected_price_one == estimated_price_sell_one
            order_quantity_two = (quantity + (second_quantity / 2))
            order_quantity_two_str = str(order_quantity_two)
            self.browser.send_keys(enter_amount_sell, order_quantity_two_str)
            time.sleep(2)
            estimated_price_sell_two = self.browser.execute_js(self.driver, self.locators.ESTIMATED_PRICE_FOR_SELL_JQ)
            expected_price_two = str(
                int(((price * quantity) + (second_price * second_quantity * 0.5)) / order_quantity_two))
            assert estimated_price_sell_two == expected_price_two
            order_quantity_three = quantity + second_quantity
            order_quantity_three_str = str(order_quantity_three)
            self.browser.send_keys(enter_amount_sell, order_quantity_three_str)
            time.sleep(2)
            estimated_price_sell_three = self.browser.execute_js(self.driver, self.locators.ESTIMATED_PRICE_FOR_SELL_JQ)
            expected_price_three = str(
                int(((price * quantity) + (second_price * second_quantity)) / order_quantity_three))
            assert estimated_price_sell_three == expected_price_three
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    def tearDown(self):
        Browser.close_browser(self.driver)
