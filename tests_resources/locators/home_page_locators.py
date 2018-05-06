# !/usr/bin/env python
# -*- coding: utf8 -*-
from tests_resources.locators.base_page_locators import BasePageLocators


class HomePageLocators(BasePageLocators):
    SETTINGS_DROPDOWN = "//*[@class='dropdown-toggle'][contains(text(),'XAISupervisor ')]"
    LOGOFF_BUTTON = "//*[@role='menuitem'][contains(text(),'  Logoff ')]"
    HOME_PAGE_LABEL = "//*[@class='label label-success'][contains(.,'ME-ADMIN')]"
    LOGOFF_CONFIRM_BUTTON = "//button[@tests_data-bb-handler='confirm'][contains(text(),'OK')]"
    
    