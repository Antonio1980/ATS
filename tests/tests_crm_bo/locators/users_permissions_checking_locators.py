COMMUNICATOR_MENU_ID = "menu-Communicator"   # "//*[@id='menu-Communicator']"
COMMUNICATOR_MENU = "//*[@id='menu-Communicator']"
SCHEDULED_MESSAGING_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Scheduled Messaging')]"
CAMPAIGNS_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Campaigns')]"
TEMPLATES_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Templates')]"
SCHEDULED_MESSAGING_PAGE_TITLE = "//*[@id='content']//div[@class='page-subHeader-text pull-left'][contains(.,'Scheduled Messaging')]"
CAMPAIGNS_PAGE_TITLE = "//*[@id='content']//div[@class='page-subHeader-text pull-left'][contains(.,'Campaigns')]"
TEMPLATES_PAGE_TITLE = "//*[@id='content']//div[@class='page-subHeader-text pull-left'][contains(.,'Templates')]"
ADD_TEMPLATE_BUTTON_ID = "addTemplate" # "//*[@id="addTemplate"]"
ADD_TEMPLATE_BUTTON = "//*[@id='addTemplate']"
ADD_CAMPAIGN_BUTTON = "//*[@id='content']//a[@class='btn btn-default'][contains(.,'Add campaign')]"
ADD_NEW_SCHEDULED_MESSAGE_ID = "addNewMessage"  # "//*[@id="addNewMessage"]"
ADD_NEW_SCHEDULED_MESSAGE = "//*[@id='addNewMessage']"
EDIT_SCHEDULED_MESSAGE_LINK = "//*[@id='scheduledMessagesTable']/tbody/tr[@class='odd']/td[1]/a[@class='editMessageLink']"     ####
EDIT_TITLE_ON_EDIT_PAGE_SHEDULED_MESSAGE = "//*[@id='addEditQ']//div[@class = 'panel-heading p1'][contains(.,'Edit')]"
EDIT_CAMPAIGN_LINK = "//*[@id='DataTables_Table_0']/tbody/tr[1]/td[@class=' sorting_1']/a[@class='btn btn-link']"             ###
TEMPLATES_NO_RECORDS_TO_DISPLAY = "//*[@id='dynamicTemplateTable']//td[@class='dataTables_empty'][contains(.,'No records to display')]"
EDIT_TEMPLATES_LINK = "//*[@id='editTemplate']"
EDIT_TITLE_ON_EDIT_PAGE_TEMPLATES = "//*[@id='ngmailertemplates']//h4/span[contains(.,'Edit Template')]"
CREATE_TITLE_NEW_CAMPAIGN_PAGE = "//*[@id='form-validate']//span[contains(.,'Campaigns: New campaign')]"
CREATE_NEW_SCHEDULED_MEASSAGE_TITLE_ON_SCHEDULED_MESSAGING_PAGE = "//*[@id='addEditQ']//span[contains(.,'Create New Scheduled Message')]"
NOT_EDIT_TEMPLATES = "//*[@id='id-45']/td[1]"
NOT_EDIT_CAMPAIGN = "//*[@id='DataTables_Table_0']/tbody/tr[1]/td[@class=' sorting_1']"




NOT_EDIT_SCHEDULED_MESSAGE = "//*[@id='scheduledMessagesTable']//td"
EDIT_TITLE_ON_EDIT_PAGE_CAMPAIGNS = "//*[@id='form-validate']//span[contains(.,'Edit campaign')]"




# customers
CUSTOMER_MENU = "//*[@id='main-navigation']/ul[@class='navigation']//a[contains(.,'Customers')]"
QUICK_CUSTOMER_APPROVAL_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Quick Customers Approval')]"
SEARCH_CUSTOMER_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Search')]"
QUICK_SEARCH_DROPDOWN_BUTTON = "//*[@id='quick-search-container']//button[@data-id ='quick-search-type']"
QUICK_SEARCH_BUTTON = "//*[@id='quick-search-button']"
QUICK_SEARCH_VALUE_FIELD = "//*[@id='quick-search-value']"
QUICK_CUSTOMER_APPROVAL_TITLE_ON_QUICK_CUSTOMER_APPROVAL_PAGE = "//*[@id='content']//div[@class = 'page-subHeader-text pull-left'][contains(.,'Quick Customers Approval')]"
SEARCH_CUSTOMER_TITLE_ON_SEARCH_CUSTOMER_PAGE = "//*[@id='content']//div[@class = 'page-subHeader-text pull-left'][contains(.,'Search')]"

#reports
REPORTS_MENU_ID = "menu-Reports"   # //*[@id="menu-Reports"]
REPORTS_MENU = "//*[@id='menu-Reports']"
Q_MANAGER_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Q Manager')]"
Q_STATISTICS_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Q Statistics')]"
GROUPS_CHANGES_HISTORY_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Groups Changes History')]"
USERS_CHANGES_HISTORY_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Users Changes History')]"
Q_MANAGER_TITLE_ON_Q_MANAGER_PAGE = "//*[@id='content']//div[@class = 'page-subHeader-text pull-left'][contains(.,'Q Manager')]"
Q_STATISTICS_TITLE_ON_Q_STATISTICS_PAGE = "//*[@id='content']//div[@class = 'page-subHeader-text pull-left'][contains(.,'Q Statistics')]"
PERMISSION_GROUPS_CHANGES_HISTORY_ON_GROUPS_CHANGE_HISTORY = "//*[@id='content']//div[@class = 'page-subHeader-text pull-left'][contains(.,'Permission Groups Changes History')]"
USERS_CHANGES_HISTORY_ON_USERS_CHANGE_HISTORY = "//*[@id='content']//div[@class = 'page-subHeader-text pull-left'][contains(.,'Users Changes History')]"

#management
MANAGEMENT_MENU_ID = "menu-index"   # //*[@id="menu-index"]
MANAGEMENT_MENU = "//*[@id='menu-index']"
USERS_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Users')]"
PERMISSIONS_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Permissions')]"
DESKS_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Desks')]"
CUSTOMER_STATUS_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Customer Status')]"
USERS_TITLE_ON_USER_PAGE = "//*[@id='content']//div[@class='page-subHeader-text pull-left'][contains(.,'Users')]"
PERMISSIONS_TITLE_ON_PERMISSIONS_PAGE = "//*[@id='content']//div[@class='page-subHeader-text pull-left'][contains(.,'Permissions')]"
DESKS_TITLE_ON_DESKS_PAGE = "//*[@id='content']//div[@class='page-subHeader-text pull-left'][contains(.,'Desks')]"
CUSTOMER_STATUS_TITLE_ON_CUSTOMER_STATUS_PAGE = "//*[@id='content']//div[@class='page-subHeader-text pull-left'][contains(.,'Customer Status')]"
EDIT_TITLE_ON_EDIT_USERS_PAGE = "//*[@id='add_user_form']//div[@class='panel-heading p1'][contains(.,'Edit')]"
CREATE_USER_BUTTON_ON_USERS_PAGE = "//*[@id='createUser']"
EDIT_LINK_FOR_USER = "//*[@id='mainEmployeeTable']//a"     #return set of links
EDIT_LINK_FOR_PERMISSIONS = "//*[@id='DataTables_Table_0']//a" #return set of links
CREATE_PERMISSIONS_GROUP_BUTTON = "//*[@id='addGroup']"
EDIT_LINK_FOR_DESKS = "//*[@id='deskTable']//a" #return set of links

CLOSE_BUTTON_ON_MODAL_FOR_EDIT_DESKS = "//*[@id='myModal']//button[@class='close']"
NOT_EDIT_DESKS = "//*[@id='deskTable']//td"
CREATE_DESKS_BUTTON = "//*[@id='desk-save-button']"
EDIT_LINK_CUSTOMER_STATUS = "//*[@id='table-results']//a" #return set of links

NOT_EDIT_CUSTOMER_STATUS = "//*[@id='table-results']//td" #return set of links
CREATE_NEW_CUSTOMER_STATUS_BUTTON = "//*[@id='new-status']"
CREATE_MODAL_NEW_CUSTOMER_STATUS_TITLE = "//*[@id='action-title'][contains(.,'Create New Customer Status')]"
EDIT_TITLE_ON_EDIT_PERMISSIONS_GROUP_PAGE = "//*[@id='mainDiv']//div[@class='panel-heading p1'][contains(.,'Edit')]"
EDIT_MODAL_FOR_DESKS = "//*[@id='myModal']//div[@class='modal-content'][contains(.,'Edit')]"
EDIT_MODAL_FOR_CUSTOMER_STATUS = "//*[@id='action-title']"
CLOSE_BUTTON_ON_MODAL_FOR_EDIT_CUSTOMER_STATUS = "//*[@id='status-action-modal']//button[@class='close']"
NOT_EDIT_USERS = "//*[@id='mainEmployeeTable']//td"   #return set of links
CREATE_NEW_USER_TITLE_ON_USERS_PAGE = "//*[@id='add_user_form']/div/div/div[@class='panel-heading p1'][contains(., 'Create New User')]"
CREATE_MODAL_NEW_DESK = "//*[@id='deskmodal'][contains(.,'Add new desk')]"
CREATE_NEW_PERMISSIONS_GROUP_TITLE_ON_CREATE_NEW_PERMISSIOMS_GROUP_PAGE = "//*[@id='mainDiv']//div[@class='panel-heading p1']//span[contains(.,'Create New Permission Group')]"
CHECKBOX_FOR_CREATE_OPTION_OF_COMMUNICATOR_PERMISSIONS_DISABLED = "//*[@id='createCheckBox_M:11_PE:18'][@disabled='disabled']"
CHECKBOX_FOR_CREATE_OPTION_OF_COMMUNICATOR_PERMISSIONS = "//*[@id='createCheckBox_M:11_PE:18']"


#customer related actions
CUSTOMER_ID_LIST = "//*[@id='customersDataTable']//a"  #return set of links
COMMUNICATION_ID_LIST = "//*[@id='communicationTable']//td"  #return set of links
COMMUNICATIONS_TAB_ID = "communications_tab"  #//*[@id="communications_tab"]
COMMUNICATION_TITLE_ON_COMMUNICATIONS_PAGE = "//*[@id='dynamicCommunicationTableWrap']/div[@class='panel-heading p1']//span[contains(.,'Communications')]"
ADD_COMMUNICATION_BUTTON  = "//*[@id='createCommunication']"
EDIT_LINK_COMMUNICATIONS_LIST = "//*[@id='communicationTable']//a"
MODAL_EDIT_COMMUNICATIONS = "//*[@id='communicationPopUpWindow']//div[@class='modal-header']/h4[contains(.,Edit)]"
CLOSE_BUTTON_ON_MODAL_FOR_EDIT_COMMUNICATION = "//*[@id='communicationPopUpWindow']//button[@class='close']"
NEW_COMMUNICATION_TITLE_ON_MODAL = "//*[@id='communicationPopUpWindow']//h4[contains(.,'New Communication')]"
EDIT_MAIL_ON_QUICK_CUSTOMERS_APPROVAL = "//*[@id='editEmail']"
QUICK_CUSTOMERS_APPROVAL_TITLE_ON_QUICK_CUSTOMERS_APPROVAL_PAGE = "//*[@id='content']//div[@class = 'page-subHeader-text pull-left'][contains(.,'Quick Customers Approval')]"
SEND_EMAIL_TITLE_ON_MODAL_WIN = "//*[@id='send-email-customer']//span[contains(.,'Send Email To ')]"
DEPOSITS_WITHDRAWALS_DROPDOWN_TITLE = "//*[@id='main-navigation']//ul[contains(@style,'display: block')]//a[contains(.,'Deposits & Withdrawals')]"
DEPOSITS_WITHDRAWALS_TITLE_ON_DEPOSITS_WITHDRAWL_PAGE = "//*[@id='content']//div[@class = 'page-subHeader-text pull-left'][contains(.,'Deposits & Withdrawals')]"
CUSTOMER_ID_LIST_ON_DEPOSITS_PAGE = "//*[@id='depositsDataTable']//a"  #return set of links
DEPOSITS_WITHDRAWLS_TITLE_TAB_ON_CUSTOMER_PAGE = "//*[@id='dw_tab']"
NOT_EDIT_ID_DEPOSITS_ON_CUSTOMER_PAGE = "//*[@id='depositsDataTable']//tr[@class='odd']/td"   #return set of links
EDIT_ID_DEPOSITS_LINK_ON_CUSTOMER_PAGE = "//*[@id='depositsDataTable']//span[@class='depositsDataId']"  #return set of links
EDIT_DEPOSIT_DETAILS_TITLE_ON_MODAL_WIN = "//*[@id='edittransactiontitle']"
CLOSE_BUTTON_ON_MODAL_FOR_EDIT_DEPOSIT = "//*[@id='edittransactionmodal']//button[@class='close']"
ADD_NEW_DEPOSIT_BUTTON = "//*[@id='newdeposit']"
NEW_DEPOSIT_REQUEST_TITLE_ON_MODAL_WINNEW = "//*[@id='transactiontitle']"
DEPOSITS_TITLE_ON_DEPOSITS_BLOCK = "//*[@id='customer_dw']//h4/span[contains(.,'Deposits')]"
WITHDRAWALS_TITLE_ON_WITHDRWALS_BLOCK = "//*[@id='customer_dw']//h4/span[contains(.,'Withdrawals')]"
CUSTOMER_ID_LIST_ON_WITHDRAWALS_PAGE = "//*[@id='withdrawalsDataTable']//a" #return set of links
NOT_EDIT_ID_WITHDRAWALS_ON_CUSTOMER_PAGE = "//*[@id='withdrawalsDataTable']//td"  #return set of links
EDIT_ID_WITHDRAWALS_LINK_ON_CUSTOMER_PAGE = "//*[@id='withdrawalsDataTable']//span[@class='withdrawalsDataId']"
ADD_NEW_WITHDRAWAL_BUTTON = "//*[@id='newwithdrawal']"
EDIT_WITHDRAWAL_DETAILS_TITLE_ON_MODAL_WIN = "//*[@id='edittransactiontitle']"
CLOSE_BUTTON_ON_MODAL_FOR_EDIT_WITHDRAWAL = "//*[@id='edittransactionmodal']//button[@class='close']"
ADD_NEW_WITHDRAWAL_REQUEST_TITLE_ON_MODAL_WIN = "//*[@id='transactiontitle']"


#customer page
CUSTOMER_ADMIN_TAB_ID = "customer_admin_status_tab"                            #  "//*[@id='customer_admin_status_tab']"
ADDITIONAL_INFORMATION_TAB = "//*[@id='statusTab']//span[@class='medText'][contains(.,'Additional Information')]"
ADDITIONAL_INFORMATION_CONTENT = "//*[@id='customer-admin-additional-container']"
FIRST_NAME_DISABLED_IN_PERSONAL_INFORMATION = "//*[@id='setFirstname'][@class='form-control uniform-input text disabled disabled disabled']"
KYC_TAB_ID = "kyc_tab"    # "//*[@id="kyc_tab"
NOT_EDIT_ID_DOCUMENT_FROM_KYC = "//*[@id='documentsTable']//td[@class=' sorting_1']"  #return set of ID
EDIT_ID_DOCUMENT_FROM_KYC = "//*[@id='documentsTable']//a"
DELITE_BUTTON_ON_KYC = "//*[@id='delete-document']"
ADD_NEW_DOCUMENT_BUTTON_KYC = "//*[@id='new-document']"
EDIT_DOCUMENT_DETAILS_TITLE_MODAL_WIN = "//*[@id='document-action-title']"
CLOSE_BUTTON_ON_MODAL_FOR_EDIT_DOCUMENTATION_DETAILS = "//*[@id='document-action']//button[@class='close']"
ADD_NEW_DOCUMENT_TITLE_MODAL_WIN = "//*[@id='document-action-title']"


