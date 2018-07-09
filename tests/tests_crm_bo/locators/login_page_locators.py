class LogInPageLocators(object):
    #
    USERNAME_FIELD_ID = "username" #"//*[@id='username']"
    PASSWORD_FIELD_ID = "password" #"//*[@id='password']"
    LOGIN_BUTTON_ID = "loginBtn" #"//*[@id='loginBtn']"
    PASSWORD_INCORRECT_MESSAGE = "//*[@class='alert alert-danger'][contains(.,' The login details you are using are incorrect.')]"
    FORGOT_PASSWORD_LINK = "//*[@class='forgot help-block']" #"//*[@class='pull-left'][contains(.,'Forgot your password?')]"

    # Forgot password pop up
    POPUP_ID = "myModal" # //*[@id='myModal']
    POPUP_FORGOT_PASSWORD = "//div[@id='myModal'][@aria-hidden='false']//div[@class='modal-content']"
    POPUP_CHECK = "//div[@id='myModal'][@aria-hidden='true']"
    POPUP_HEADER = POPUP_FORGOT_PASSWORD + "//h3[@id='forgetheader'][contains(text(),'Forgot your password?')]"
    POPUP_SEND_BUTTON_ID = "sendMail" #"//*[@id='sendMail']"
    POPUP_SEND_BUTTON = "//*[@id='sendMail']"
    POPUP_CLOSE_BUTTON = "//button[@class='btn btn-default'][contains(text(),'Close')]"
    POPUP_EMAIL_FIELD_ID = "email" #"//input[@id='email']"
    POPUP_ERROR_MESSAGE_ID = "//span[@id='errorMsg'][contains(text(),'Please enter a valid email address')]"
    POPUP_MESSAGE = POPUP_FORGOT_PASSWORD + "//div[contains(text(),'Change your password in two easy steps. This helps to keep your new password secure.')]"
    POPUP_NOTE_MESSAGE = POPUP_FORGOT_PASSWORD + "//p[contains(text(),'Note that in order to use this features, you must already have a valid email address and be an active user.')]"

    # Email sent pop up
    EMAIL_POPUP = "//*[@class='modal-content']"
    EMAIL_POPUP_HEADER = "//*[@class='modal-body']"
    EMAIL_SENT_POPUP_HEADER = "forgetheader"
    EMAIL_MESSAGE_ID = "errorMsg"
    EMAIL_POPUP_CLOSE_BUTTON = "//*[@class='btn btn-default'][contains(text(),'Close')]"
