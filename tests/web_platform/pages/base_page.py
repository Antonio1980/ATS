# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.browser import Browser
from src.test_definitions import BaseConfig


class BasePage(Browser):
    @classmethod
    def set_up_base_page(cls):
        cls.base_url = BaseConfig.WTP_BASE_URL

    @classmethod
    def go_to_home_page(cls):
        cls.go_to_url(cls.wtp_home_page_url)