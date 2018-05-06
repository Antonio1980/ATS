# !/usr/bin/env python
# -*- coding: utf8 -*-
from tests_resources.locators.base_page_locators import BasePageLocators


class HomePageLocators(BasePageLocators):
    SETTINGS_DROPDOWN = "//i[@class='fas fa-cogs fa-2x']"
    LOGOFF_BUTTON = "//*[@id='header-user-info-signout'][@class='pull-left']/a[contains(.,'Sign Out')]"
    HOME_PAGE_LOGO = "//*[@class='pull-left brandLogoOverride'][@id='brandLogo']"
    #LOGOFF_CONFIRM_BUTTON = "//button[@tests_data-bb-handler='confirm'][contains(text(),'OK')]"
    
    