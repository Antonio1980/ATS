# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.browser import Browser
from src.test_definitions import BaseConfig


class BasePage(Browser):
    @classmethod
    def setup_base_page(cls):
        cls.base_url = BaseConfig.CRM_BASE_URL
