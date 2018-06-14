<<<<<<< a6ac884835aaa047de5b5f6bf0e391f6806c43ed:tests/me_admin/pages/base_page.py
# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.browser import Browser
from src.test_definitions import BaseConfig


class BasePage(Browser):
    def __init__(self):
        self.me_base_url = BaseConfig.CRM_BASE_URL
=======
# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.browser import Browser


class BasePage(Browser):
    def __init__(self):
        self.page_elements = ['el1','el2','el3']
>>>>>>> 46d3ea0049230292881d76fb45bbfa6fde5f95e8:tests/tests_me_admin/pages/base_page.py
