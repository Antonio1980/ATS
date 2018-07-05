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
    PASSWORD_ERROR = "//*[@class='password']/div[@class='error fieldError hidden']/span"
    TERM_OF_USE_LINK = "//a[@class='termOfUse']"
    PRIVACY_POLICY_LINK = "//a[@class='privacyPolicy']"
    SIGNIN_LINK = "//a[@class='custom loginLink']"
    EMAIL_ERROR = "//div[@class='email']/div[@class='error fieldError hidden']/span"

    # Verify your email screen
    EMAIL_NOT_ARRIVED = "//*[@class='resendBtn']"
    EMAIL_ALREADY_VERIFIED = "//*[@class='reSyncBtn']"
    GO_BACK_TO_DX = "//*[@class='emailVerification hidden']//a[@href='/']"
    
    