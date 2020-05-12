import unittest
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.crm_tests_base.customer_page import CustomerPage
from tests.crm_tests_base.locators import permissions_locators


@ddt
class TestCommunicator(unittest.TestCase):
    def setUp(self):
        self.test_case = '0'
        self.username = "Christina K"
        self.password = "qwerty12345"
        self.home_page = HomePage()
        self.login_page = LogInPage()
        self.customer_page = CustomerPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.customer_id = self.login_page.customer_id
        self.locators = permissions_locators

    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_communicator_permission_test(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        step1, step2, step3 = False, False, False
        try:
            step1 = self.home_page.set_communicator_option_to_menu()
            step2 = self.login_page.login(self.driver, self.username, self.password)
            assert Browser.find_element_by(self.driver, self.locators.COMMUNICATOR_MENU_ID, "id")
            # assert Browser.check_element_not_presented(self.driver, self.locators.CUSTOMER_MENU, delay)
            # assert Browser.check_element_not_presented(self.driver, self.locators.REPORTS_MENU, delay)
            # assert Browser.check_element_not_presented(self.driver, self.locators.MANAGEMENT_MENU, delay)
            step3 = True
        finally:
            if step1 and step2 and step3 is True:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "1 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                # Instruments.write_file_step(self.test_case + "," + self.test_run + "," + "0 \n", self.results_file)
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
