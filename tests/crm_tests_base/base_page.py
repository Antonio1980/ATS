from src.base.browser import Browser
from src.base import crm_base_url, logger
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.locators import base_page_locators


class BasePage(Browser):
    
    def __init__(self):
        super(BasePage, self).__init__()
        self.crm_base_url = crm_base_url
        self.base_locators = base_page_locators
        self.crm_username = BaseConfig.CRM_USERNAME
        self.crm_password = BaseConfig.CRM_PASSWORD
        self.phone = Instruments.get_faked_phone()
        self.ui_delay = float(BaseConfig.CRM_DELAY)
        self.crm_users_file = Instruments.get_data(BaseConfig.CRM_TESTS_USERS)
        self.customers_file = Instruments.get_data(BaseConfig.WTP_TESTS_CUSTOMERS)

    @automation_logger(logger)
    def go_back_and_wait(self, driver, previous_url):
        self.go_back(driver)
        return self.wait_url_contains(driver, previous_url, self.ui_delay)
