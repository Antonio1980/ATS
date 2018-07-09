import string
import random
from src.base.browser import Browser
from tests.test_definitions import BaseConfig
from tests.tests_crm_bo.locators.base_page_locators import BasePageLocators


class BasePage(Browser):
    def __init__(self):
        super(BasePage, self).__init__()
        self.crm_base_url = BaseConfig.CRM_STAGING_URL
        self.customer_id = BaseConfig.CRM_CUSTOMER_ID
        self.base_locators = BasePageLocators()

    def email_generator(self, size=8, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))
