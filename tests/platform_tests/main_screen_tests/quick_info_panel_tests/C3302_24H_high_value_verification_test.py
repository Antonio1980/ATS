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

test_case = '3302'


@allure.title("QUICK INFO PANEL")
@allure.description("""
    UI test.
    ""24H High" - value verification", UI
    1. Open WTP
    2. Get date 24 hours ago
    3. Get max price in the last 24 hours from db 
    4. Get 24h High from ui and compare with max price from db(from 3 step). They must be equal.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='"24H High" - value verification"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/quick_info_panel_tests/C3304_24H_volume_value_verification_test.py",
                 "TestVerificationValue24HHigh")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", "web_driver")
@pytest.mark.ui
@pytest.mark.quick_info_panel
class TestVerificationValue24HHigh(object):
    browser = Browser()
    home_page = HomePage()
    delay = home_page.ui_delay
    main_screen_page = MainScreenPage()
    locators = main_screen_page.locators
    instrument_id = 1007
    redis_24_h_high = None

    @allure.step("Starting with: test_sign_in")
    @automation_logger(logger)
    def test_sign_in(self, web_driver):
        self.home_page.open_home_page(web_driver)
        time.sleep(self.delay)

    @allure.step("Starting with: test_get_redis_24_h_high")
    @automation_logger(logger)
    def test_get_redis_24_h_high(self):
        TestVerificationValue24HHigh.redis_24_h_high = RedisDb.get_ticker_high_24(self.instrument_id)
        assert self.redis_24_h_high is not None

    @allure.step("Proceed with: test_get_24h_volume_from_ui")
    def test_get_24h_volume_from_ui(self, r_customer, web_driver):
        self.browser.execute_js(self.driver,
                                '''$('li[data-instrumentId=''' + str(self.instrument_id) + ''']').click()''')
        time.sleep(5.0)
        ui_24h_high = float(self.browser.get_attribute_from_locator(web_driver, self.locators.HIGH_24_QUICK_PANEL,
                                                                    'innerText'))
        assert ui_24h_high == self.redis_24_h_high
        logger.logger.info("ui_24h_high {0} == redis_24_h_high {1}".format(ui_24h_high, self.redis_24_h_high))

        logger.logger.info("==================== TEST {0} IS PASSED ====================".format(test_case))
