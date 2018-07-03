class HomePageLocators(object):
    # Home page header
    SETTINGS_DROPDOWN = "//i[@class='fas fa-cogs fa-2x']"
    LOGOUT_LINK = "//*[@id='header-user-info-signout'][@class='pull-left']/a[contains(.,'Sign Out')]"
    HOME_PAGE_LOGO_ID = "brandLogo" # "//*[@class='pull-left brandLogoOverride '][@id='brandLogo']"
    HOME_PAGE_LOGO = "//*[@class='pull-left brandLogoOverride'][@id='brandLogo']"
    SIDE_BAR = "//*[@id='header-user-info-settings-sidebar-inner']"
    LANGUAGE_ICON = "//span[@class='bfh-selectbox-option']/i[@class='glyphicon bfh-flag-US']"
    # Home page body (dashboard)
    CUSTOMER_DROPDOWN = "//span[@class='filter-option pull-left'][contains(.,'Customer Name')]"
    CUSTOMER_ID_OPTION = "//*[@class='text'][contains(text(),'Customer ID')]"
    CUSTOMER_NAME_FIELD_ID = "quick-search-value"  # "//*[@id='quick-search-value']"
    SHOW_RESULTS_BUTTON_ID = "quick-search-button"  # //*[@id='quick-search-button'][@data-original-title='Show Results']
    #
    MANAGEMENT_DROPDOWN_ID = "menu-index"
    MANAGEMENT_DROPDOWN = "//*[@id='menu-index']"
    MANAGEMENT_USERS_OPTION = "//*[@class='subPage'][@href='/dx/users/']"
    MANAGEMENT_PERMISSION_OPTION = "//*[@class ='subPage'][@href='/dx/permissions/']"
    MANAGEMENT_DESKS_OPTION = "//*[@class ='subPage'][@href='/dx/desks']"
    MANAGEMENT_CUSTOMER_STATUS_OPTION = "//*[@class ='subPage'][@href='/dx/customerStatus']"
    #
    COMMUNICATOR_DROPDOWN_ID = "menu-Communicator"
    COMMUNICATOR_SCHEDULED_MESSAGING_OPTION = "//*[@class='subPage'][@href='/dx/scheduled-messaging']"
    COMMUNICATOR_DROPDOWN_CAMPAINGS = "//*[@class='subPage'][@href='/dx/campaigns']"
    COMMUNICATOR_TAMPLATES_OPTION = "//*[@class='subPage'][@href='/dx/communicator']"
    #
    REPORTS_DROPDOWN_ID = "menu-Reports"
    REPORTS_Q_MANAGER_OPTION = "//*[@class='subPage'][@href='dx/showreport/getReport/Q%20Manager']"
    REPORTS_Q_STATISTICS_OPTION = "//*[@class='subPage'][@href='dx/showreport/getReport/Q%20Statistics']"
    REPORTS_GROUPS_CHANGES_HISTORY_OPTION = "//*[@class='subPage'][@href='/dx/reports/permissionGroupsChangesHistory']"
    REPORTS_USERS_CHANGES_HISTORY_OPTION = "//*[@class='subPage'][@href='/dx/reports/usersChangesHistory']"
