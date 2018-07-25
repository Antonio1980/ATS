class ForgotPasswordPageLocators(object):
    FORGOT_PASSWORD_TITLE = "//*[@class='forgotInfo']" # [contains(text(),'Please enter your verified Email address')]
    EMAIL_TEXT_FIELD = "//input[@class='popupTextInput'][@name='email']"
    SUBMIT_BUTTON = "//input[@class='forgotPasswordSubmit formButton'][@value='Submit']"
    ERROR_MESSAGE = "//*[@id='forgotPasswordForm']/div[@class='generalFormError generalFormMessage hidden']"
    EMAIL_ERROR_MESSAGE = "//*[@class='fieldError emailError hidden']/span[@class='errorText']"
    TEXT = "//*[@class='resetMessage formBox hidden']/div[@class='text']"
    CAPTCHA = "//*[@id='recaptcha-anchor']"
    MESSAGE = "//*[@class='resetMessage formBox hidden'][@style='display: block;']"

    # Forgot Password New Page (Reset Password)
    PASSWORD_FIELD = "//input[@name='password']"
    CONFIRM_PASSWORD_FIELD = "//input[@name='confirmedPassword']"
    CONFIRM_BUTTON = "//input[@value='Confirm']"
    PASSWORD_ERROR = "//*[@class='passwordError fieldError hidden'][@style='display: none;']"
    CONFIRM_PASSWORD_ERROR = "//*[@class='error fieldError hidden'][@style='display: none;']"
    CONTINUE_BUTTON = "//*[@class='continueButton formButton']"
