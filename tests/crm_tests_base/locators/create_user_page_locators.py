FIRST_NAME_ID = "userFirstNameInput"  # //*[@id='userFirstNameInput']
LAST_NAME_ID = "userLastNameInput"  # //*[@id='userLastNameInput']
EMAIL_ID = "userEmailInput"  # //*[@id='userEmailInput']
PHONE_ID = "userPhoneInput"  # //*[@id='userPhoneInput']
USERNAME_ID = "userNameInput"  # //*[@id='userNameInput']
CREATE_USER_BUTTON_ID = "user-save-button"
CREATE_USER_BUTTON = "//*[@id='user-save-button']"
USER_PERMISSION_ID = "userPermInput"  # //*[ @id='userPermInput']
USER_STATUS_ID = "userStatusInput"  # //*[@id='userStatusInput']
USER_TYPE_ID = "userTypeInput"  # //*[@id='userTypeInput']
RESET_PASSWORD_BUTTON_ID = "reset-password-button"  # //*[@id='reset-password-button']

LANGUAGE_DROPDOWN = "//*[@data-id='userLanguageSelect']"
LANGUAGE_FIELD = "//*[@class='btn-group bootstrap-select open']//div[@class='bs-searchbox']"
LANGUAGE_TEXT_FIELD = "//*[@class='btn-group bootstrap-select open']//div[@class='bs-searchbox']/input"

PERMISSION_GROUP_DROPDOWN = "//button[@data-id='userPermInput']"
PERMISSION_GROUP_FIELD = "//*[@class='dropdown-menu open'][@style='max-height: 322px; overflow: hidden;']/*[@class='bs-searchbox']"
PERMISSION_GROUP_TEXT_FIELD = "(//input[@class='form-control uniform-input text'])[3]"

STATUS_DROPDOWN = "//*[@data-id='userStatusInput']"
STATUS_FIELD = "//*[@class='btn-group bootstrap-select open']//div[@class='bs-searchbox']"
STATUS_TEXT_FIELD = "//*[@class='btn-group bootstrap-select open']//input"

USER_TYPE_DROPDOWN = "//*[@data-id='userTypeInput']"
USER_TYPE_FIELD = "//*[@class='btn-group bootstrap-select open']//div[@class='bs-searchbox']"
USER_TYPE_TEXT_FIELD = "//*[@class='btn-group bootstrap-select open']//span[contains(.,'Admin')]"

# PAYMENT_METHOD_DROPDOWN = "//button[@data-id='paymentMethod']//span[@class='filter-option pull-left'][contains(text(),'Nothing Selected')]"
# CREDIT_CARD_OPTION = "//*[@class='text'][contains(text(),'Credit Card')]"
# CLEARING_COMPANY_DROPDOWN = "//button[@data-id='clearingCompany']//span[@class='filter-option pull-left'][contains(text(),'Nothing Selected')]"

DESKS_DROPDOWN = "//button[@data-id='userDesksInput']/span[@class='filter-option pull-left']"
DESKS_FIELD = ""
DESKS_TEXT_FIELD = ""

# UI locators
PAGE_TITLE_1 = "//div[@class='page-header-text pull-left']"
PAGE_TITLE_2 = "//div[@class='page-subHeader-text pull-left']"
NEW_USER_HEADER = "//a[@class='minimize']"
PASSWORD_MESSAGE = "//div[@class='col-lg-12']"

# Field errors
FIRST_NAME_ERROR = "//*[@for='userFirstNameInput'][@class='error']"
LAST_NAME_ERROR = "//*[@for='userLastNameInput'][@class='error']"
EMAIL_ERROR = "//*[@for='userEmailInput'][@class='error']"
PHONE_ERROR = "//*[@for='userPhoneInput'][@class='error']"
USERNAME_ERROR = "//*[@for='userNameInput'][@class='error']"
