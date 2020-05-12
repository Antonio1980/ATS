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

test_case = '3304'
instrument_id = 1036


@allure.title("QUICK INFO PANEL")
@allure.description("""
    UI test.
    "Verification Value "24H Volume", UI
    1. Open WTP
    2. Get total quantity of the buy trades from last 24 hours from redis
    3. Get 24h volume from ui and compare with total quantity from redis(from 3 step). They must be equal.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Verification value "24 Hour Volume"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/quick_info_panel_tests/C6260_verification_value_24_hour_volume_test.py",
                 "TestVerificationValue24HVolume")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", "web_driver")
@pytest.mark.ui
@pytest.mark.quick_info_panel
class TestVerificationValue24HVolume(object):
    browser = Browser()
    home_page = HomePage()
    main_screen_page = MainScreenPage()
    delay = main_screen_page.ui_delay
    locators = main_screen_page.locators
    redis_volume_24 = None

    @allure.step("Starting with: test_sign_in")
    @automation_logger(logger)
    def test_sign_in(self, web_driver):
        self.home_page.open_home_page(web_driver)
        time.sleep(self.delay)

    @allure.step("Starting with: test_get_volume_redis")
    @automation_logger(logger)
    def test_get_volume_redis(self):
        TestVerificationValue24HVolume.redis_volume_24 = RedisDb.get_ticker_volume_24(instrument_id)
        assert self.redis_volume_24 is not None

    @allure.step("Proceed with: test_get_24h_volume_from_ui")
    def test_get_24h_volume_from_ui(self, r_customer, web_driver):
        self.browser.execute_js(web_driver, '''$('li[data-instrumentId=''' + str(instrument_id) + ''']').click()''')
        time.sleep(5.0)
        ui_24h_volume = float(
            self.browser.find_element(web_driver, self.locators.VOLUME_24_QUICK_PANEL).get_attribute('innerText'))
        assert ui_24h_volume == round(self.redis_volume_24, 2)
        logger.logger.info("ui_24h_volume {0} == redis_volume_24 {1}".format(ui_24h_volume, self.redis_volume_24))
        
        logger.logger.info("==================== TEST {0} IS PASSED ====================".format(test_case))
