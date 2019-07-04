import time
import unittest

import allure
import pytest
from ddt import ddt, data, unpack

from config_definitions import BaseConfig
from src.base import logger
from src.base.customer.registered_customer import RegisteredCustomer
from src.base.data_bases.redis_db import RedisDb
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.main_screen_page import MainScreenPage
from tests.platform_tests_base.signin_page import SignInPage

test_case = '6252'


@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    "Verification Value "Last Price", UI
    1. Open WTP
    2. Select some quoted currency on the main assets panel. (BTC)
    3. Select some base currency. (DXCASH/BTC)
    4. Find the price of the last instrument's trade in redis.
    5. Get value of "last price" field on the platform.
    6. Verify that Price from redis equal Price on the platform
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Verification Value "Last Price"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/asset_panel_tests/C6252_verification_value_last_price_test.py",
                 "TestVerificationValueLastPrice")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.ui
@pytest.mark.asset_panel
@ddt
class TestVerificationValueLastPrice(unittest.TestCase):
    @allure.step("SetUp:  calling of registered customer.")
    @automation_logger(logger)
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.main_screen_page = MainScreenPage()
        self.locators = self.main_screen_page.locators
        self.browser = self.customer.get_browser_functionality()
        self.instrument_id = "1026"

    @allure.step("Starting with: test_verification_value_last_price")
    @automation_logger(logger)
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_verification_value_last_price(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = self.home_page.ui_delay
        assert self.home_page.open_signin_page(self.driver)
        assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
        assert self.browser.wait_element_presented(self.driver, self.locators.UPPER_RULER, delay)
        btc = self.browser.wait_element_presented(self.driver, self.locators.BTC_CURRENCY_NOT_SELECTED, delay)
        self.browser.click_on_element(btc)
        last_price = RedisDb.get_ticker_last_price(self.instrument_id)
        time.sleep(3)
        last_price_from_ui = self.browser.find_element(
            self.driver, "//*[@id='dx_platform']//li[@data-instrumentid = '" + str(
                self.instrument_id) + "']//div[@class = 'commonPrice']").get_attribute(
            'innerText')
        assert float(last_price) == float(last_price_from_ui)
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        self.browser.close_browser(self.driver)
