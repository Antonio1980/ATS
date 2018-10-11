from src.base.browser import Browser
from test_definitions import BaseConfig


class BasePage(Browser):
    def __init__(self):
        super().__init__(self)
        self.me_base_url = BaseConfig.ME_BASE_URL
