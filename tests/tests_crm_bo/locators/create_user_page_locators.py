# !/usr/bin/env python
# -*- coding: utf8 -*-


class CreateUserPageLocators(object):

    FIRST_NAME_ID = "userFirstNameInput" # //*[@id='userFirstNameInput']
    LAST_NAME_ID = "userLastNameInput" # //*[@id='userLastNameInput']
    EMAIL_ID = "userEmailInput" # //*[@id='userEmailInput']
    PHONE_ID = "userPhoneInput" # //*[@id='userPhoneInput']
    USERNAME_ID = "userNameInput" # //*[@id='userNameInput']
    CREATE_USER_BUTTON_ID = "user-save-button" # //*[@id='user-save-button']
    USER_PERMISSION_ID = "userPermInput" # //*[ @id='userPermInput']
    USER_STATUS_ID = "userStatusInput" # //*[@id='userStatusInput']
    USER_TYPE_ID = "userTypeInput" # //*[@id='userTypeInput']

    LANGUAGE_DROPDOWN = "//*[@data-id='userLanguageSelect']"
    LANGUAGE_FIELD = "//*[@class='btn-group bootstrap-select open']//div[@class='bs-searchbox']"
    LANGUAGE_TEXT_FIELD = "//*[@class='btn-group bootstrap-select open']//div[@class='bs-searchbox']/input"

    PERMISSION_GROUP_DROPDOWN = "//button[@data-id='userPermInput'][@title='None Selected']"
    PERMISSION_GROUP_FIELD = "//*[@class='dropdown-menu open'][@style='max-height: 322px; overflow: hidden;']/*[@class='bs-searchbox']"
    PERMISSION_GROUP_TEXT_FIELD = "(//INPUT[@type='text'])[5]"

    STATUS_DROPDOWN = "//*[@data-id='userStatusInput']"
    STATUS_FIELD = "//*[@class='btn-group bootstrap-select open']//div[@class='bs-searchbox']"
    STATUS_TEXT_FIELD = "//*[@class='btn-group bootstrap-select open']//input"

    USER_TYPE_DROPDOWN = "//*[@data-id='userTypeInput']"
    USER_TYPE_FIELD = "//*[@class='btn-group bootstrap-select open']//div[@class='bs-searchbox']"
    USER_TYPE_TEXT_FIELD = "//*[@class='btn-group bootstrap-select open']//input"

    #PAYMENT_METHOD_DROPDOWN = "//button[@data-id='paymentMethod']//span[@class='filter-option pull-left'][contains(text(),'Nothing Selected')]"
    #CREDIT_CARD_OPTION = "//*[@class='text'][contains(text(),'Credit Card')]"
    #CLEARING_COMPANY_DROPDOWN = "//button[@data-id='clearingCompany']//span[@class='filter-option pull-left'][contains(text(),'Nothing Selected')]"

