import time

import allure
import pytest

from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.main_screen_page import MainScreenPage
from tests.platform_tests_base.signin_page import SignInPage

test_case = '6251'


@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    Sorting Functionality, UI
    1. Open Home Page 
    2. Verify that filter presents correct data if input full asset name
    3. Verify that filter presents correct data if input part of asset name
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Sorting Functionality')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/asset_panel_tests/C6251_asset_search_test.py",
                 "TestSortingFunctionality")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", "web_driver")
@pytest.mark.ui
@pytest.mark.asset_panel
class TestAssetSearch(object):
    browser = Browser()
    home_page = HomePage()
    sign_in_page = SignInPage()
    main_screen_page = MainScreenPage()
    delay = main_screen_page.ui_delay
    locators = main_screen_page.locators

    @allure.step("Starting with: test_open_home_page")
    @automation_logger(logger)
    def test_open_home_page(self, web_driver):
        self.home_page.open_home_page(web_driver)
        time.sleep(self.delay)

    @allure.step("Proceed with: test_filter_full_name ")
    @automation_logger(logger)
    def test_filter_full_name(self, web_driver):
        search_box = self.browser.wait_element_presented(web_driver, self.locators.SEARCH_BOX, self.delay)
        assert search_box
        query = 'btc'
        self.browser.input_data(search_box, query)
        filtering_assets = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        filtering_list = self.main_screen_page.get_all_base_names(filtering_assets)
        for item in filtering_list:
            assert query.upper() in item

    @allure.step("Proceed with: test_filter_part_of_name ")
    @automation_logger(logger)
    def test_filter_part_of_name(self, web_driver):
        search_box = self.browser.wait_element_presented(web_driver, self.locators.SEARCH_BOX, self.delay)
        assert search_box
        query = 'b'
        self.browser.input_data(search_box, query)
        filtering_assets = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        filtering_list = self.main_screen_page.get_all_base_names(filtering_assets)
        for item in filtering_list:
            assert query.upper() in item
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
