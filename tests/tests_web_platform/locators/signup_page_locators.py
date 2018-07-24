class SignUpPageLocators(object):
    OPEN_ACCOUNT_FRAME = "//*[@id='platformAuthDialog']"
    OPEN_ACCOUNT_BOX_ID = "openAccountDxForm"
    OPEN_ACCOUNT_BOX = "//*[@id='openAccountDxForm']"
    OPEN_ACCOUNT_LOGO = "//*[@class='registration hidden']/div[@class='title']"
    FIRST_NAME_FIELD = "//input[@name='firstName'][@placeholder='First name']"
    LAST_NAME_FIELD = "//input[@name='lastName'][@placeholder='Last name']"
    EMAIL_FIELD = "//input[@name='email'][@placeholder='Email address']"
    PASSWORD_FIELD = "//input[@name='password'][@placeholder='Password']"
    CAPTCHA = "//input[@name='captcha']" # "//div[@class='recaptcha-checkbox-checkmark'][@role='presentation']"
    CAPTCHA_FRAME = "//*[@class='g-recaptcha']//iframe"
    CAPTCHA_MAIN_FRAME = "//*[@class='g-recaptcha'][@data-theme='light']"
    CREATE_ACCOUNT_BUTTON = "//*[@class='registration-form-wrapper']//input[@class='formButton']" # "//input[@class='formButton'][@value='Create Account']"
    NEWSLETTERS_CHECKBOX = "//div[@class='receivePromoEmail']//span[@class='checkmark']"
    CERTIFY_CHECKBOX = "//div[@class='acceptTerms']//span[@class='checkmark']"
    # "//*[@class='password']/div[@class='error fieldError hidden']/span"
    PASSWORD_ERROR = "//*[@id='openAccountDxForm']/div[@class='password']//div[@class='error fieldError hidden']"
    TERM_OF_USE_LINK = "//a[@class='termOfUse']"
    PRIVACY_POLICY_LINK = "//a[@class='privacyPolicy']"
    SIGNIN_LINK = "//a[@class='custom loginLink']"
    # "//div[@class='email']/div[@class='error fieldError hidden']/span"
    EMAIL_ERROR = "//*[@id='openAccountDxForm']/div[@class='email']//div[@class='error fieldError hidden']"

    # Verify your email screen
    EMAIL_NOT_ARRIVED = "//*[@class='resendBtn']"
    EMAIL_ALREADY_VERIFIED = "//*[@class='reSyncBtn']"
    GO_BACK_LINK = "//*[@class='emailVerification hidden']//a[@href='/']"

    # Add phone number screen
    SELECT_COUNTRY_DROPDOWN = "//a[@class='chzn-single chzn-default']/span"
    SELECT_COUNTRY_FIELD = "//div[@class='chzn-search']/input"
    PHONE_FIELD = "//div[@class='phoneNumber']/input[@name='phone']"
    PHONE_PREFIX = "//div[@class='phoneNumber']/input[@name='phonePrefix']"
    SEND_BUTTON = "//input[@value='Send']"
    GO_BACK_LINK_P = "//*[@class='validatePhoneNumber hidden']/div[@class='subscription']/a"
    
    # Verify phone number screen
    CODE_FIELD = "//input[@name='code']"
    SUBMIT_BUTTON = "//input[@value='Submit']"
    RESEND_LINK = "//*[@class='resend']"
    ANOTHER_PHONE_LINK = "//*[@class='resetPhone']/a"

    # Personal details screen
    NEXT_BUTTON = "//*[@id='openAccountDxDetailsForm']/div/div[1]/input"
    NAME_FIELD = "//*[@name='firstName'][@placeholder='First name']"
    DATE_OF_BIRTH = "//input[@class='formField hasDatepicker']"
    CALENDAR_TABLE = "//table[@class='ui-datepicker-calendar']"
    CALENDAR = "//*[@id='ui-datepicker-div']"
    CALENDAR_ID = "ui-datepicker-div"
    DATE = "//a[@class='ui-state-default'][contains(.,'')]"
    MONTH_SELECT = "//select[@class='ui-datepicker-month']"
    YEAR_SELECT = "//select[@class='ui-datepicker-year']"
    DAY = "//td[@class=' ui-datepicker-week-end ']/a[@class='ui-state-default'][contains(.,'2')]"
    CITY_FIELD = "//input[@name='city']"
    ZIP_FIELD = "//input[@name='postCode']"
    ADDRESS_FIELD = "//input[@name='street']"
    ADDRESS_2_FIELD = "//input[@name='streetTwo']"
    US_CHECKNOX = "//div[@class='uSTaxReportable']//span[@class='checkmark']"
    POLITICAL_CHECKBOX = "//div[@class='politicallyExposed']//span[@class='checkmark']"

    # Client Checklist 1
    EMPLOYMENT_DROPDOWN= "//*[@class='employmentStatusTr']//a"
    EMPLOYMENT_OPTIONS = "//*[@class='employmentStatusTr']//li"
    BUSINESS_NAME_INPUT = "//input[@name='businessNameEmployed']"
    OCCUPATION_INPUT = "//input[@name='occupationEmployed']"
    BUSINESS_YEAR_INPUT = "//input[@name='businessSetupYear']"
    INDUSTRY_DROPDOWN = "//*[@class='industrySectorEmployedTr']//a[@class='chzn-single chzn-default']"
    INDUSTRY_OPTIONS = "//*[@class='industrySectorEmployedTr']//li"
    NEXT_BUTTON_CHECKLIST1 = "//*[@id='dxPackageContainer_openAccountDx']//div[@class='dynamicQuestions hidden']//li[@class='stepContainer hidden step_1']//input[@class='submitInput']"

    # Client Checklist 2
    ANNUAL_INCOME = "//*[@class='annualIncomeTr']//a"
    ANNUAL_OPTIONS = "//*[@class='annualIncomeTr']//li"
    SOURCE_SELECT = "//*[@class='sourceOfDealingFundsTr']//a"
    SOURCE_OPTIONS = "//*[@class='sourceOfDealingFundsTr']//li"
    INHERITANCE_CHECKBOX = "//*[@for='mainActivityGeneratedWealth_65']/span[@class='checkmark']"
    NEXT_BUTTON_CHECKLIST2 = "//*[@class='stepContainer hidden step_2']//td[@class='submitTd']/input"

    # Client Checklist 3
    DOCUMENTS = "//div[@class='uploadText']"
    DOCUMENT_1 = "//*[@class='doc_1_1_0Hidden hidden']"
    DOCUMENT_2 = "//*[@class='doc_1_2_0Hidden hidden']"
    DOCUMENT_3 = "//*[@class='doc_2_1_0Hidden hidden']"
    NEXT_BUTTON_CHECKLIST3 = "//*[@id='openAccountUploadDocumentsForm']//input[@class='formButton']"

    FINISH_BUTTON = "//*[@class='registerDone hidden']//input"

    
