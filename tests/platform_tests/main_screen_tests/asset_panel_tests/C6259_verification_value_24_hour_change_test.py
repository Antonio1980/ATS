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

test_case = '6259'


@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    "Verification Value "24H Change", UI
    1. Open WTP
    2. Get last trade price from Redis
    3. Get 24h change from ui and compare with 24h Change from Redis(from 2 step). They must be equal.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Verification value "24 Hour Change"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/asset_panel_tests/C6259_verification_value_24_hour_change_test.py",
                 "TestVerificationValue24HChange")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", "r_customer", "web_driver")
@pytest.mark.ui
@pytest.mark.asset_panel
class TestVerificationValue24HChange(object):
    browser = Browser()
    home_page = HomePage()
    main_screen_page = MainScreenPage()
    delay = main_screen_page.ui_delay
    locators = main_screen_page.locators
    instrument_id = 1022
    redis_change = None

    @allure.step("Starting with: test_open_home_page")
    @automation_logger(logger)
    def test_open_home_page(self, web_driver):
        self.home_page.open_home_page(web_driver)
        time.sleep(self.delay)

    @allure.step("Proceed with: test_get_24_h_change_value_from_ui")
    @automation_logger(logger)
    def test_get_24_h_change_value_from_redis(self):
        TestVerificationValue24HChange.redis_change = round((RedisDb.get_ticker_change_24(self.instrument_id)), 2)
        assert self.redis_change is not None

    @allure.step("Proceed with: test_get_24_h_change_value_from_ui")
    @automation_logger(logger)
    def test_get_24_h_change_value_from_ui(self, web_driver):
        change_locator = self.main_screen_page.generate_x_path_for_change(self.instrument_id)
        ui_24h_change = float(self.browser.find_element(web_driver, change_locator).get_attribute('innerText'))
        assert ui_24h_change == self.redis_change
        logger.logger.info("redis_change {0} ==  ui_24h_change {1}".format(self.redis_change, ui_24h_change))
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
