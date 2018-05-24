# !/usr/bin/env python
# -*- coding: utf8 -*-


class HomePageLocators():
    SETTINGS_DROPDOWN = "//*[@class='dropdown-toggle'][contains(.,'XAISupervisor ')]"
        #"//*[@class='dropdown-toggle'][contains(text(),'XAISupervisor ')]/span[@class='caret']"
    LOGOFF_BUTTON = "//*[@role='menuitem'][contains(text(),'  Logoff ')]"
    HOME_PAGE_LABEL = "//*[@class='label label-success'][contains(.,'ME-ADMIN')]"
    LOGOFF_CONFIRM_BUTTON = "//button[@tests_data-bb-handler='confirm'][contains(text(),'OK')]"