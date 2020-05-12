import time
import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signin_page import SignInPage
from src.base.customer.registered_customer import RegisteredCustomer
from tests.platform_tests_base.main_screen_page import MainScreenPage

test_case = '5674'


@allure.title("Maintenance Time")
@allure.description("""
    Verification of some elements exist at the screen during maintenance time, UI test
    1. Get me-state 
    2. Verify that me-state equal 2 (Maintenance time)
    3. Open WTP with registered customer
    4. Verify that Asset Panel - without price, instead of price -present 3 dots
    5. At the Trade area (include: graph, quick info panel, limit and market panels, 
    ability to cancel orders from Open orders panel) hold an image with the general message.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='End of Day Maintenance message at the Web Platform')
@allure.testcase(
    BaseConfig.GITLAB_URL +
    "/maintenance_time_tests/C5674_end_of_day_maintenance_message_presented_test.py",
    "TestEndOfDayMaintenanceMessageWebPlatform")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.maintenance_time
@ddt
class TestEndOfDayMaintenanceMessageWebPlatform(unittest.TestCase):
    @automation_logger(logger)
    @allure.step("SetUp: calling registered customer and get me-state.")
    def setUp(self):
        self.home_page = HomePage()
        self.sign_in_page = SignInPage()
        self.customer = RegisteredCustomer()
        self.main_screen = MainScreenPage()
        self.locators = self.main_screen.locators
        self.browser = self.customer.get_browser_functionality()
        self.delay = 5.0
        self.state_me = Instruments.get_me_state()

    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    @allure.step("Starting with: test_end_of_day_maintenance_message_web_platform")
    def test_end_of_day_maintenance_message_web_platform(self, browser):
        assert self.state_me == 2
        self.driver = WebDriverFactory.get_driver(browser)
        assert self.home_page.open_signin_page(self.driver)
        assert self.sign_in_page.sign_in(self.driver, self.customer.email, self.customer.password)
        time.sleep(10)
        assert self.browser.wait_element_presented(self.driver, self.locators.LEFT_BAR_ASSET_PANEL, self.delay)

        assert self.browser.find_element_by(self.driver, self.locators.UPPER_RULER_ID, "id")
        assert self.browser.wait_element_presented(self.driver, self.locators.CURRENT_PORTFOLIO_VALUE, self.delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.ORDERS_INFO_PANEL, self.delay)
        assert self.browser.check_element_not_presented(self.driver, self.locators.TRADE_SECTION, self.delay)
        assert self.browser.check_element_not_presented(self.driver, self.locators.ORDERS_INFO_PANEL, self.delay)
        assert self.browser.wait_element_presented(self.driver, self.locators.MAINTENANCE_TEXT, self.delay)
        logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
        logger.logger.info("==================== TEST IS PASSED ====================")

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        Browser.close_browser(self.driver)
