class BasePageLocators(object):
    SIGN_UP_BUTTON = "//*[@class='signUpLink']"
    LOGIN_BUTTON = "//*[@class='loginButton']"
    LOGIN_BUTTON_CLS = "loginButton"
    SIGN_UP_BUTTON_CLS = "signUpLink"

    CHANGE_PASSWORD_BUTTON = "//a[contains(text(),'Change Password')]"
    VERIFY_EMAIL_BUTTON = "//a[contains(text(),'Verify Email')]"  # //tbody/tr[2]/td/table/tbody/tr[3]/td/a
    PAUSE_BUTTON_ID = "play_button" # "//*[@id='play_button']"
    EMAIL_FRAME_ID = "msg_body" # "//*[@id='msg_body']"
    FIRST_EMAIL = "//*[@id='inboxpane']/li[1]"

