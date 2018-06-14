# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.browser import Browser
from tests.test_definitions import BaseConfig


class BasePage(Browser):
    def __init__(self):
        self.wtp_base_url = BaseConfig.WTP_BASE_URL
