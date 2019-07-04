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

test_case = '6927'


@allure.feature("Limit Order")
@allure.title("Limit Panel")
@allure.description("""
    UI test.
    "Plus" and "Minus" buttons validation for "Buy" and "Sell" sections, UI
    1. Open WTP
    2. Select an instrument(1012).
    3. Click on the "Plus" button in the "Buy" section. Expected result: The price presented on the "Buy" button 
    is increased by 1/(10^significantDigit).
    4. Click on the "Minus" button in the "Buy" section. Expected result: The price presented on the "Buy" button is
      decreased by 1/(10^significantDigit)
    5. Click on the "Plus" button in the "Sell" section. Expected result: The price presented on the "Sell" button 
      is increased by 1/(10^significantDigit).
    6. Click on the "Minus" button in the "Sell" section. Expected result: The price presented on the "Sell" button is
      decreased by 1/(10^significantDigit).
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Plus" and "Minus" buttons.')
@allure.testcase(BaseConfig.GITLAB_URL + "/main_screen_tests/limit_order_panel_tests/C6927_plus_and_minus_buttons_test.py",
    "TestPlusAndMinusButton")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.limit_order
@pytest.mark.order_management
@ddt
class TestPlusAndMinusButton(unittest.TestCase):
    @allure.step("SetUp: calling registered customer.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.limit_order_panel = LimitOrderPanelPage()
        self.locators = self.limit_order_panel.locators
        self.browser = self.customer.get_browser_functionality()

    @allure.step("Starting with: test_plus_and_minus_buttons")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_plus_and_minus_buttons(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_plus_and_minus_buttons with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        delay, result = self.home_page.ui_delay, 0
        try:
            assert self.home_page.open_signin_page(self.driver)
            assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
            usd_title_menu = self.browser.wait_element_presented(self.driver, self.locators.USD, delay)
            self.browser.click_on_element(usd_title_menu)
            eur_from_dropdown = self.browser.wait_element_presented(self.driver,
                                                                    self.locators.EUR_OPTION_FROM_USD_DROPDOWN,
                                                                    delay)
            self.browser.click_on_element(eur_from_dropdown)

            self.browser.execute_js(self.driver, '''$('li[data-instrumentId=1012]').click()''')
            time.sleep(10.0)

            significant_digit_tail = int(
                Instruments.run_mysql_query("SELECT significantDigit FROM assets WHERE id = 6")[0][0])
            increases_button_buy = self.browser.wait_element_presented(self.driver,
                                                                       self.locators.INCREASES_STEP_BUTTON_BUY, delay)
            estimated_price_before_increase_buy = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_BUY_JQ)
            self.browser.click_on_element(increases_button_buy)
            time.sleep(2)

            estimated_after_increase_buy = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_BUY_JQ)
            step_of_increase_decreases = 1 / (10 ** significant_digit_tail)
            assert (round((float(estimated_price_before_increase_buy) + step_of_increase_decreases),
                          significant_digit_tail) == float(estimated_after_increase_buy))

            decreases_button_buy = self.browser.wait_element_presented(self.driver,
                                                                       self.locators.DECREASES_STEP_BUTTON_BUY, delay)
            self.browser.click_on_element(decreases_button_buy)
            time.sleep(2)

            estimated_after_decreases_buy_jq = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_BUY_JQ)
            assert (float(estimated_after_decreases_buy_jq) ==
                    round((float(estimated_after_increase_buy) - step_of_increase_decreases), significant_digit_tail))

            increases_button_sell = self.browser.wait_element_presented(self.driver,
                                                                        self.locators.INCREASES_STEP_BUTTON_SELL, delay)
            estimated_before_increase_sell = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_SELL_JQ)
            self.browser.click_on_element(increases_button_sell)
            time.sleep(2)
            estimated_after_increase_sell = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_SELL_JQ)
            assert (round((float(estimated_before_increase_sell) + step_of_increase_decreases), significant_digit_tail)
                    == float(estimated_after_increase_sell))

            decreases_button_sell = self.browser.wait_element_presented(self.driver,
                                                                        self.locators.DECREASES_STEP_BUTTON_SELL, delay)
            self.browser.click_on_element(decreases_button_sell)
            time.sleep(2)
            estimated_after_decreases_sell_jq = self.browser.execute_js(self.driver, self.locators.ENTER_PRICE_SELL_JQ)
            assert (float(estimated_after_decreases_sell_jq) ==
                    round((float(estimated_after_increase_sell) - step_of_increase_decreases), significant_digit_tail))
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
