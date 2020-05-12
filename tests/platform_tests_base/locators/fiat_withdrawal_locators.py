FUNDS_BUTTON = "//*[@id='dx_header']//div[@class = 'headerBtn accountStatus_funds' ]"
WITHDRAWAL_BUTTON_EUR = "//*[@id='2']//button[@class = 'withdrawal']"
INPUT_WITHDRAWAL_AMOUNT = "//form[@class='withdrawalWireForm']//input[@name = 'amount']"
INPUT_DESCRIPTION = "//form[@class='withdrawalWireForm']//input[@name = 'description']"
INPUT_NAME_ON_ACCOUNT_INPUT = "//form[@class='withdrawalWireForm']//input[@name = 'accountName']"
INPUT_IBAN = "//form[@class='withdrawalWireForm']//input[@name = 'iban']"
INPUT_BANK_NAME = "//*[@id='2']//input[@name = 'bankName']"
INPUT_BIC = "//form[@class='withdrawalWireForm']//input[@name = 'bic']"
INPUT_ADDRESS = "//form[@class='withdrawalWireForm']//input[@name = 'address']"
EUR_TITLE_ON_WITHDRAWAL_PAGE = "//*[@id='dx_fundsBalance']//div[@class='currency'][contains(.,'EUR')]"
SUBMIT_BUTTON_WITHDRAWAL = "//form[@class='withdrawalWireForm']//div[@class='footer']//button[@class = 'formButton submitBtn']"
LIST_OF_ERRORS_IF_NO_INPUT_FOR_WITHDRAWAL = "//form[@class='withdrawalWireForm']//div[@class='error hidden'][contains(@style,'display: block')]"
CONFIRMATION_CODE_PAGE_FOR_EUR = "//*[@id='2']//form[@class= 'smsConfirmationForm']"
ENTER_CONFIRMATION_CODE_FOR_EUR = "//*[@id='2']//input[@name = 'smsCode']"
SUCCESSFUL_WITHDRAWAL_PAGE_EUR = "//*[@id='2']/div[@class='smsConfirmationContainer hidden']/div[@class='generalFormSuccess generalFormMessage hidden']"
FINISH_BUTTON_EUR = "//*[@id='2']/div[@class='smsConfirmationContainer hidden']/div[@class='generalFormSuccess generalFormMessage hidden']/button[@class='formButton finishBtn']"

#jquery locators
EUR_CURRENCY_TOTAL_BALANS_FUNDS_PAGE_JQ = '''return $("[id='2'] td[class = 'fundsTotalBalance']").text();'''
TEXT_MESSAGE_JQ = '''return $("[id='msgs'] tr:contains(AUTHMSG@) td[data-label='Message:']").text();'''
EUR_CURRENCY_AVAILABLE_BALANS_FUNDS_PAGE_JQ = '''return $("[id='2'] td[class = 'fundsAvailableBalance']").text();'''
