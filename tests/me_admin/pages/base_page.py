# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.browser import Browser
from src.test_definitions import BaseConfig


class BasePage(Browser):
    def __init__(self):
        self.me_base_url = BaseConfig.CRM_BASE_URL
