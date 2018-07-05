class CustomerPageLocators(object):
    # customer page locators
    CUSTOMER_ID_TEXT = "//*[@class='customerIdtext'][contains(text(),'Customer ID ')]"
    DEPOSIT_WITHDRAWALS_INSET_ID = "dw_tab" # //*[@id="dw_tab"]
    BALANCE_INSET_ID = "balance_tab" # //*[@id='balance_tab']
    ADD_DEPOSIT_BUTTON_ID = "newdeposit" # //*[@id='newdeposit']
    CUSTOMER_ICON_ID = "customerGroupIcon" # //*[@id='customerGroupIcon']
    # new deposit pop up
    NEW_DEPOSIT_POPUP = "//*[@id='transactionmodal'][@aria-hidden='false']"
    NEW_DEPOSIT_POPUP_TITLE_ID = "transactiontitle" # //*[@id='transactiontitle'][contains(text(),'New Deposit Request')]
    PAYMENT_METHOD_DROPDOWN = "//button[@data-id='paymentMethod']//span[@class='filter-option pull-left'][contains(text(),'Nothing Selected')]"
    CREDIT_CARD_OPTION = "//*[@class='text'][contains(text(),'Credit Card')]"
    CLEARING_COMPANY_DROPDOWN = "//button[@data-id='clearingCompany']//span[@class='filter-option pull-left'][contains(text(),'Nothing Selected')]"
    ALL_CHARGE_TRANS_OPTION = "//span[@class='text'][contains(text(),'AllCharge')]"
    TRANSACTION_STATUS_DROPDOWN = "//button[@data-id='trasactionStatus']//span[@class='filter-option pull-left'][contains(text(),'Nothing Selected')]"
    STATUS_OPTION = "//li[@data-original-index='2']//span[@class='text'][contains(text(),'Approved')]" # "//*[@data-original-index='2'][@class='selected active']//span[@class='text'][contains(text(),'Approved')]"
    CURRENCY_DROPDOWN = "//button[@data-id='currency']//span[@class='filter-option pull-left'][contains(text(),'Nothing Selected')]"
    CURRENCY_OPTION = "//*[@class='text'][contains(text(),'USD')]"
    AMOUNT_FIELD_ID = "amount" # //*[@id='amount']
    REFERENCE_NUMBER_FIELD_ID = "referenceNumber" # //*[@id='referenceNumber']
    COMMENTS_FIELD_ID = "comments" # //*[@id='comments']
    BIN_CARD_NUMBER_FIELD_ID = "binNumber" # //*[@id='binNumber']
    CC_CARD_NUMBER_FIELD_ID = "ccEnd" # //*[@id='ccEnd']
    SAVE_BUTTON_ID = "transactionSaveButton" # //*[@id='transactionSaveButton']




    
    

    

























