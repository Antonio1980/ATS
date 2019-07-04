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

test_case = '3300'


@allure.title("QUICK INFO PANEL")
@allure.description("""
    UI test.
    "Verification Value "24H Change", UI
    1. Open WTP
    2. Get  Value 24 h Change from Redis
    3. Get 24h change from ui and compare with 24h Change from db(from 2 step). They must be equal.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Verification value "24 Hour Change"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/quick_info_panel_tests/C3300_24H_change_value_verification_test.py",
                 "TestVerificationValue24HChange")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", "web_driver")
@pytest.mark.ui
@pytest.mark.quick_info_panel
class TestVerificationValue24HChange(object):
    browser = Browser()
    home_page = HomePage()
    main_screen_page = MainScreenPage()
    delay = main_screen_page.ui_delay
    locators = main_screen_page.locators
    instrument_id = 1022
    redis_change = None

    @allure.step("Starting with: test_sign_in")
    @automation_logger(logger)
    def test_sign_in(self, web_driver):
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
        self.browser.execute_js(web_driver,
                                '''$('li[data-instrumentId=''' + str(self.instrument_id) + ''']').click()''')
        ui_24h_change = float(self.browser.find_element(
            web_driver, self.locators.CHANGE_24_QUICK_PANEL).get_attribute('innerText')[:-1])
        a = self.browser.execute_js(web_driver, self.locators.NEGATIVE_CHANGE)
        if a:
            ui_24h_change = -ui_24h_change
        assert ui_24h_change == self.redis_change
        logger.logger.info("ui_24h_change {0} == redis_change {1}".format(ui_24h_change, self.redis_change))
        logger.logger.info("Test {0}".format(test_case))

        logger.logger.info("==================== TEST IS PASSED ====================")
