# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.browser import Browser
from tests.test_definitions import BaseConfig


class BasePage(Browser):
    crm_base_url = BaseConfig.CRM_INTEGRATION_URL

    def __init__(self):
        super(BasePage, self).__init__()