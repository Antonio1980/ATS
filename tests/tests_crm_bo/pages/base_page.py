import string
import random
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import get_account_details
from tests.tests_crm_bo.locators.base_page_locators import BasePageLocators


class BasePage(Browser, BaseConfig):
    def __init__(self):
        super(BasePage, self).__init__()
        self.base_locators = BasePageLocators()
        self.crm_base_url = self.CRM_STAGING_URL
        # data_file, row, column1, column2, column3
        self.account_details = get_account_details(BaseConfig.WTP_TESTS_CUSTOMERS, 0, 0, 1, 2)
        self.customer_id = self.account_details['customer_username']

    def email_generator(self, size=8, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))
