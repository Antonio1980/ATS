import time
import allure
import pytest
from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.data_bases.redis_db import RedisDb
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.main_screen_page import MainScreenPage

test_case = '2857'
instrument_id = 1026


@allure.title("QUICK INFO PANEL")
@allure.description("""
    UI test.
    "Verification Value "Last Price", UI
    1. Open WTP
    2. Select some quoted currency on the main assets panel. 
    3. Select some base currency.
    4. Find the price of the last instrument's trade in DB.
    5. Get value of "last price" field on the platform.
    6. Verify that Price from DB equal Price on the platform
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"Last Trade " - value verification')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/quick_info_panel_tests/C2857_last_trade_value_verification_test.py",
                 "TestVerificationValueLastPrice")
@pytest.mark.usefixtures("r_time_count", 'web_driver')
@pytest.mark.ui
@pytest.mark.quick_info_panel
class TestVerificationValueLastPrice(object):
    browser = Browser()
    home_page = HomePage()
    main_screen_page = MainScreenPage()
    delay = main_screen_page.ui_delay
    locators = main_screen_page.locators

    @allure.step("Starting with: test_verification_value_last_price")
    @automation_logger(logger)
    def test_verification_value_last_price(self, web_driver):
        self.home_page.open_home_page(web_driver)
        assert self.browser.wait_element_presented(web_driver, self.locators.UPPER_RULER, self.delay + 10.0)
        self.browser.execute_js(web_driver, '''$('li[data-instrumentId=''' + str(instrument_id) + ''']').click()''')
        last_price = RedisDb.get_ticker_last_price(instrument_id)
        time.sleep(5.0)
        last_price_from_ui = self.browser.get_attribute_from_locator(web_driver,
                                                                     self.locators.BASE_RATE_QUICK_PANEL, 'innerText')
        assert float(last_price) == float(last_price_from_ui)
        logger.logger.info("last_price {0} == last_price_from_ui {1}".format(last_price, last_price_from_ui))
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
