from src.base.browser import Browser
from tests.test_definitions import BaseConfig


class BasePage(Browser):
    def __init__(self):
        super(BasePage, self).__init__()
        self.me_base_url = BaseConfig.ME_BASE_URL
