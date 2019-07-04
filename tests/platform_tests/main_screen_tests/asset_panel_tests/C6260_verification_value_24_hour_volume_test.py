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

test_case = '6260'
instrument_id = 1049


@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    "Verification Value "24H Volume", UI
    1. Open WTP
    2. Get date 24 hours ago
    3. Get total quantity of the buy trades from last 24 hours from redis 
    4. Get 24h volume from ui and compare with total quantity from redis(from 3 step). They must be equal.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Verification value "24 Hour Volume"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/asset_panel_tests/C6260_verification_value_24_hour_volume_test.py",
                 "TestVerificationValue24HVolume")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", "web_driver")
@pytest.mark.ui
@pytest.mark.asset_panel
class TestVerificationValue24HVolume(object):
    browser = Browser()
    home_page = HomePage()
    main_screen_page = MainScreenPage()
    locators = main_screen_page.locators
    delay = main_screen_page.ui_delay
    redis_volume_24 = None

    @allure.step("Starting with: test_open_home_page")
    @automation_logger(logger)
    def test_open_home_page(self, web_driver):
        self.home_page.open_home_page(web_driver)
        time.sleep(self.delay)

    @allure.step("Starting with: test_get_volume_redis")
    @automation_logger(logger)
    def test_get_volume_redis(self):
        TestVerificationValue24HVolume.redis_volume_24 = RedisDb.get_ticker_volume_24(instrument_id)
        assert self.redis_volume_24 is not None

    @allure.step("Proceed with: test_get_24h_volume_from_ui")
    def test_get_24h_volume_from_ui(self, r_customer, web_driver):
        volume_locator = self.main_screen_page.generate_x_path_for_volume(instrument_id)
        ui_24h_volume = float(self.browser.find_element(web_driver, volume_locator).get_attribute('title'))
        assert ui_24h_volume == self.redis_volume_24
        logger.logger.info("ui_24h_volume {0} == redis_volume_24 {1}".format(ui_24h_volume, self.redis_volume_24))
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
