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

test_case = '6247'


@allure.title("ASSET PANEL")
@allure.description("""
    UI test.
    "Asset Panel - Favorites", UI
    1. Open Home Page 
    2. Set some favorite assets on UI
    3. Click in Favorite Icon (Star) on UI
    4. Generate list of favorite assets from UI
    5. Compare list_1 that were set in 2 step with List_2 of Favorite assets from UI. 
       List_1 must exist in List_2
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Asset Panel - Favorites"')
@allure.testcase(BaseConfig.GITLAB_URL +
                 "/main_screen_tests/asset_panel_tests/C6247_favorites_test.py",
                 "TestFavorites")
@pytest.mark.incremental
@pytest.mark.usefixtures("r_time_count", "web_driver", "r_customer")
@pytest.mark.ui
@pytest.mark.asset_panel
class TestFavorites(object):
    browser = Browser()
    home_page = HomePage()
    sign_in_page = SignInPage()
    main_screen_page = MainScreenPage()
    delay = main_screen_page.ui_delay
    locators = main_screen_page.locators
    favorite_list = None
    favorite_list_2 = None

    @allure.step("Starting with: test_sign_in")
    @automation_logger(logger)
    def test_sign_in_page(self, web_driver, r_customer):
        self.home_page.open_signin_page(web_driver)
        time.sleep(3.0)
        self.sign_in_page.sign_in(web_driver, r_customer.email, r_customer.password)
        time.sleep(self.delay)

    @allure.step("Proceed with: test_set_favorite_assets ")
    @automation_logger(logger)
    def test_set_favorite_assets(self, web_driver):
        some_currencies = (self.browser.find_elements(web_driver, self.locators.ALL_CURRENCIES))[:5]
        TestFavorites.favorite_list = self.main_screen_page.set_favorites(some_currencies, self.browser)
        assert self.favorite_list is not None

    @allure.step("Proceed with: test_get_favorite_assets_ui ")
    @automation_logger(logger)
    def test_get_favorite_assets_ui(self, web_driver):
        star = self.browser.wait_element_presented(web_driver, self.locators.STAR_ICON_FAV, self.delay)
        self.browser.click_on_element(star)
        time.sleep(2.0)
        favorite_assets_list = self.browser.find_elements(web_driver, self.locators.ALL_FAVORITE_ASSETS)
        TestFavorites.favorite_list_2 = self.main_screen_page.get_all_base_names(favorite_assets_list)
        assert self.favorite_list_2 is not None

    @allure.step("Proceed with:test_check_favorite_assets ")
    @automation_logger(logger)
    def test_check_favorite_assets(self, web_driver):
        assert set(self.favorite_list) <= set(self.favorite_list_2)
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
