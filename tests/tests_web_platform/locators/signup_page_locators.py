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
    PASSWORD_ERROR = "//*[@id='openAccountDxForm']/div[@class='password']//div[@class='error fieldError hidden'][@style='display: block;']"
    TERM_OF_USE_LINK = "//a[@class='termOfUse']"
    PRIVACY_POLICY_LINK = "//a[@class='privacyPolicy']"
    SIGNIN_LINK = "//a[@class='custom loginLink']"
    # "//div[@class='email']/div[@class='error fieldError hidden']/span"
    EMAIL_ERROR = "//*[@id='openAccountDxForm']/div[@class='email']//div[@class='error fieldError hidden'][@style='display: block;']"

    # Verify your email screen
    EMAIL_NOT_ARRIVED = "//*[@class='resendBtn']"
    EMAIL_ALREADY_VERIFIED = "//*[@class='reSyncBtn']"
    GO_BACK_LINK = "//*[@class='emailVerification hidden']//a[@href='/']"

    # Add phone number screen
    SELECT_COUNTRY_DROPDOWN = "//a[@class='chzn-single chzn-default']"
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
    
    