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

test_case = '6250'


@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    Sorting Functionality, UI
    1. Open Home Page 
    2. Verify that 24h_volume_desc filter sorts correct
    3. Verify that 24h_volume_asc filter sorts correct
    4. Verify that 24h_change_desc filter sorts correct
    5. Verify that 24h_change_asc filter sorts correct
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Sorting Functionality')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/asset_panel_tests/C6250_sorting_functionality_test.py",
                 "TestSortingFunctionality")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", "web_driver")
@pytest.mark.ui
@pytest.mark.asset_panel
class TestSortingFunctionality(object):
    browser = Browser()
    home_page = HomePage()
    sign_in_page = SignInPage()
    main_screen_page = MainScreenPage()
    delay = main_screen_page.ui_delay
    locators = main_screen_page.locators

    @allure.step("Starting with: test_sign_in")
    @automation_logger(logger)
    def test_open_home_page(self, web_driver):
        self.home_page.open_home_page(web_driver)
        time.sleep(self.delay + 5.0)

    @allure.step("Proceed with: ")
    @automation_logger(logger)
    def test_check_24h_volume_desc(self, web_driver):
        assert self.browser.wait_element_presented(web_driver, self.locators.VOLUME_24H_DESC_SELECTED_ASSET, self.delay)
        currencies_items = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        assert currencies_items is not None
        sort_list_desc_ui = self.main_screen_page.get_all_volume(currencies_items)
        sort_list_desc = sorted(sort_list_desc_ui, reverse=True)
        assert sort_list_desc_ui == sort_list_desc

    @allure.step("Proceed with:  ")
    def test_check_24h_volume_asc(self, web_driver):
        volume_24h_desc = self.browser.wait_element_presented(web_driver, self.locators.VOLUME_24H_DESC_SELECTED_ASSET,
                                                              self.delay)
        self.browser.click_on_element(volume_24h_desc)
        time.sleep(2.0)
        assert self.browser.wait_element_presented(web_driver, self.locators.VOLUME_24H_ASC_SELECTED_ASSET, self.delay)
        currencies_items = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        sort_list_asc_ui = self.main_screen_page.get_all_volume(currencies_items)
        sort_list_asc = sorted(sort_list_asc_ui)
        assert sort_list_asc_ui == sort_list_asc

    @allure.step("Proceed with: ")
    def test_check_24h_change_desc(self, web_driver):
        change_24h = self.browser.wait_element_presented(web_driver, self.locators.CHANGE_24H_NOT_SELECTED_ASSET,
                                                         self.delay)
        self.browser.click_on_element(change_24h)
        time.sleep(2.0)
        assert self.browser.wait_element_presented(web_driver, self.locators.CHANGE_24H_DESC_SELECTED_ASSET, self.delay)
        currencies_items = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        sort_list_desc_ui = self.main_screen_page.get_all_24_h_change(currencies_items)
        sort_list_desc = sorted(sort_list_desc_ui, reverse=True)
        assert sort_list_desc_ui == sort_list_desc

    @allure.step("Proceed with:  ")
    def test_check_24h_change_asc(self, web_driver):
        change_24 = self.browser.wait_element_presented(web_driver, self.locators.CHANGE_24H_DESC_SELECTED_ASSET,
                                                        self.delay)
        self.browser.click_on_element(change_24)
        time.sleep(2.0)
        assert self.browser.wait_element_presented(web_driver, self.locators.CHANGE_24H_ASC_SELECTED_ASSET, self.delay)
        currencies_items = self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES)
        sort_list_asc_ui = self.main_screen_page.get_all_24_h_change(currencies_items)
        sort_list_asc = sorted(sort_list_asc_ui)
        assert sort_list_asc_ui == sort_list_asc
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
