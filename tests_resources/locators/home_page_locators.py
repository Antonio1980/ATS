# !/usr/bin/env python
# -*- coding: utf8 -*-
from tests_resources.locators.base_page_locators import BasePageLocators


class HomePageLocators(BasePageLocators):
    SETTINGS_DROPDOWN = "//i[@class='fas fa-cogs fa-2x']"
    LOGOUT_LINK = "//*[@id='header-user-info-signout'][@class='pull-left']/a[contains(.,'Sign Out')]"
    HOME_PAGE_LOGO = "//*[@class='pull-left brandLogoOverride'][@id='brandLogo']"
    SIDE_BAR = "//*[@id='header-user-info-settings-sidebar-inner']"
    LANGUAGE_ICON = "//span[@class='bfh-selectbox-option']/i[@class='glyphicon bfh-flag-US']"
    
    