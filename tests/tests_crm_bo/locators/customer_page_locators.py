CUSTOMER_ID_TEXT = "//*[@class='customerIdtext'][contains(text(),'Customer ID ')]"
DEPOSIT_WITHDRAWALS_INSET_ID = "dw_tab"  # //*[@id="dw_tab"]
BALANCE_INSET_ID = "balance_tab"  # //*[@id='balance_tab']
ADD_DEPOSIT_BUTTON_ID = "newdeposit"
ADD_DEPOSIT_BUTTON = "//*[@id='newdeposit']"
CUSTOMER_ICON_ID = "customerStatusIcon"  # //*[@id='customerStatusIcon']
DEPOSITOR_ICON_ID = "customerGroupIcon"  #//*[@id='customerGroupIcon']
# new deposit pop up
NEW_DEPOSIT_POPUP = "//div[@id='transactionmodal'][@class='modal fade in']//div[@class='modal-content']"
NEW_DEPOSIT_POPUP_TITLE_ID = "transactiontitle"
PAYMENT_METHOD_DROPDOWN = "//button[@data-id='paymentMethod']/span[@class='filter-option pull-left']"
PAYMENT_TEXT_INPUT = "//div[@class='btn-group bootstrap-select open']//input[@class='form-control']"
CREDIT_CARD_OPTION = "//*[@class='text'][contains(text(),'Credit Card')]"
CLEARING_COMPANY_DROPDOWN = "//button[@data-id='clearingCompany']/span[@class='filter-option pull-left']"
CLEARING_TEXT_INPUT = "//div[@class='btn-group bootstrap-select open']//input[@class='form-control']"
ALL_CHARGE_TRANS_OPTION = "//span[@class='text'][contains(text(),'AllCharge')]"
TRANSACTION_STATUS_DROPDOWN = "//button[@data-id='trasactionStatus']/span[@class='filter-option pull-left']"
STATUS_TEXT_INPUT = "//div[@class='btn-group bootstrap-select open']//input[@class='form-control']"
STATUS_OPTION = "//li[@data-original-index='2']//span[@class='text'][contains(text(),'Approved')]"
CURRENCY_DROPDOWN = "//button[@data-id='currency']//span[@class='filter-option pull-left']"
CURRENCY_TEXT_INPUT = "//div[@class='btn-group bootstrap-select open']//input[@class='form-control']"
CURRENCY_OPTION = "//*[@class='text'][contains(text(),'USD')]"
AMOUNT_FIELD_ID = "amount"  # //*[@id='amount']
VALUE_DATA_ID = "dateValueDate"   #//*[@id="dateValueDate"]
REFERENCE_NUMBER_FIELD_ID = "referenceNumber"  # //*[@id='referenceNumber']
COMMENTS_FIELD_ID = "comments"  # //*[@id='comments']
BIN_CARD_NUMBER_FIELD_ID = "binNumber"  # //*[@id='binNumber']
CC_CARD_NUMBER_FIELD_ID = "ccEnd"  # //*[@id='ccEnd']
SAVE_BUTTON_ID = "transactionSaveButton"  # //*[@id='transactionSaveButton']
WALLET_ADDRESS_ID = "walletAddress"      #//*[@id="walletAddress"]
NAME_ON_BANK_ACCOUNT_FIELD_ID = "nameBankAccount"  #//*[@id="nameBankAccount"]
IBAN_FIELD_ID = "iban"  #//*[@id="iban"]
BANK_NAME_FIELD_ID= "bankName"#//*[@id="bankName"]
BIC_FIELD_ID = "bic" #//*[@id="bic"]
BANK_ADDRESS_ID = "bankAddress"  #//*[@id="bankAddress"]
DESCRIPTION_BY_CUSTOMER = "//*[@id='customerDesc']"
CUSTOMER_BALANCE_FIELD = "//*[@id='content']//div[@class='balance']/span[contains(.,'Balance')]"
CUSTOMER_ACCOUNT_INFORMATION_AREA = "//*[@id='customer-status-wrap']"
CUSTOMER_ADMIN_TAB =  "//*[@id='customer_admin_status_tab']"
CUSTOMER_PERSONAL_INFORMATION_TAB = "//*[@id='statusTab']//a[contains(.,'Personal Information')]"
CUSTOMER_PASSWORD_ICON = "//*[@id='passwordData']"
CUSTOMER_BALANCE_TAB = "//*[@id='balance_tab']"
CUSTOMER_TRADES_TAB = "//*[@id='trades_tab']"
CUSTOMER_FEES_TAB = "//*[@id='fees_tab']"