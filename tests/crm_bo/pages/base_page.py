# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.browser import Browser
from src.test_definitions import BaseConfig


class BasePage(Browser):
    base_url = BaseConfig.CRM_BASE_URL