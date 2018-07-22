class LogInPageLocators(object):
    #
    USERNAME_FIELD_ID = "username"
    PASSWORD_FIELD_ID = "password"
    LOGIN_BUTTON_ID = "loginBtn"
    PASSWORD_INCORRECT_MESSAGE = "//*[@class='alert alert-danger'][contains(.,' The sign_in details you are using are incorrect.')]"
    FORGOT_PASSWORD_LINK = "//*[@class='forgot help-block']"

    # Forgot password pop up
    POPUP_ID = "myModal"
    POPUP_FORGOT_PASSWORD = "//div[@id='myModal'][@aria-hidden='false']//div[@class='modal-content']"
    POPUP_CHECK = "//div[@id='myModal'][@aria-hidden='true']"
    POPUP_HEADER = "//h3[@id='forgetheader'][contains(text(),'Forgot your password?')]"
    POPUP_SEND_BUTTON_ID = "sendMail"
    POPUP_SEND_BUTTON = "//*[@id='sendMail']"
    POPUP_CLOSE_BUTTON = "//button[@class='btn btn-default'][contains(text(),'Close')]"
    POPUP_EMAIL_FIELD_ID = "email"
    POPUP_EMAIL_FIELD = "//input[@id='email']"
    POPUP_ERROR_MESSAGE = "//*[@id='errorMsg']"
    POPUP_ERROR_MESSAGE_ID = "errorMsg"
    POPUP_ERROR_MESSAGE_CLOSE_BUTTON = "//*[@class='alert alert-danger']/button[@type='button']"
    POPUP_MESSAGE = "//div[contains(text(),'Change your password in two easy steps. This helps to keep your new password secure.')]"
    POPUP_NOTE_MESSAGE = "//p[contains(text(),'Note that in order to use this features, you must already have a valid email address and be an active user.')]"

    # Email sent pop up
    EMAIL_POPUP = "//*[@class='modal-content']"
    EMAIL_POPUP_HEADER = "//*[@class='modal-body']"
    EMAIL_SENT_POPUP_HEADER = "forgetheader"
    EMAIL_MESSAGE_ID = "errorMsg"
    EMAIL_POPUP_CLOSE_BUTTON = "//*[@class='btn btn-default'][contains(text(),'Close')]"

    # Change password screen
    CURRENT_PASSWORD_ID = "old_password"
    CURRENT_PASSWORD = "//input[@id='old_password']"
    NEW_PASSWORD_ID = "new_password"
    NEW_PASSWORD = "//input[@id='new_password']"
    CONFIRM_PASSWORD_ID = "confirm_password"
    CONFIRM_PASSWORD = "//input[@id='confirm_password']"
    CONFIRM_BUTTON = "//button[@type='submit']"

    # Wrong email
    PASSWORD_TOKEN_WARNING = "//*[@class='errorMessagePass danger']"
