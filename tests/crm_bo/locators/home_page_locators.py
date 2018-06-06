# !/usr/bin/env python
# -*- coding: utf8 -*-


class HomePageLocators(object):
    SETTINGS_DROPDOWN = "//i[@class='fas fa-cogs fa-2x']"
    LOGOUT_LINK = "//*[@id='header-user-info-signout'][@class='pull-left']/a[contains(.,'Sign Out')]"
    HOME_PAGE_LOGO = "//*[@class='pull-left brandLogoOverride'][@id='brandLogo']"
    SIDE_BAR = "//*[@id='header-user-info-settings-sidebar-inner']"
    LANGUAGE_ICON = "//span[@class='bfh-selectbox-option']/i[@class='glyphicon bfh-flag-US']"
    CUSTOMER_DROPDOWN = "//span[@class='filter-option pull-left'][contains(.,'Customer Name')]"
    CUSTOMER_ID_OPTION = "//*[@class='text'][contains(text(),'Customer ID')]"
    CUSTOMER_NAME_FIELD_ID = "quick-search-value"  # "//*[@id='quick-search-value']"
    SHOW_RESULTS_BUTTON_ID = "quick-search-button"  # //*[@id='quick-search-button'][@data-original-title='Show Results']
    
    
    