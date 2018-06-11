from src.base.browser import Browser
from src.test_definitions import BaseConfig


class BasePage(Browser):
    def __init__(self):
        super(BasePage, self).__init__()
        self.crm_base_url = BaseConfig.CRM_BASE_URL
