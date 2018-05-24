# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.browser import Browser


class BasePage(Browser):
    def __init__(self):
        self.page_elements = ['el1','el2','el3']